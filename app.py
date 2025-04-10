#---------APIS--------------
from flask import Flask, render_template,request, request, redirect, url_for
from flask import session
from flask import send_from_directory
from flask import jsonify,flash
from upload_handler import *
from models.create_users import *
import os


app = Flask(__name__)

# ✅ Set a secret key for sessions
app.secret_key = "your_very_secret_key_here"

UPLOAD_FOLDER = 'static/uploads'  # ✅ Save inside `static/uploads/`
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = login(username, password)  # ✅ Fetch user from DB
        if user:
            session['username'] = username
            session['role'] = user['role']  # ✅ Store role in session

            # ✅ Redirect based on role
            if user['role'] == 'admin_user':
                print("✅ Redirecting to /admin_dashboard")  
                return redirect(url_for('admin_page'))  # ✅ Admin Panel

            elif user['role'] == 'seller':
                print("✅ Redirecting to /upload")  
                return redirect(url_for('uploads_page'))  # ✅ Seller Upload Page

            elif user['role'] == 'customer':
                #print("✅ Redirecting to /home")  
                return redirect(url_for('products_page'))  # ✅ Customer Home Page
            
            else:
                print("❌ Unknown role detected!")  
                return "❌ Unknown role!", 400  # ✅ Handle unexpected roles

        else:
            print("❌ Login failed: Invalid credentials")  
            error_message = "Invalid username or password. Please try again."
            return render_template('login.html', error=error_message)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')  # Ensure role is sent from the form
        print(username,password,role)

        if not username or not password or not role:
            return "❌ All fields are required!", 400

        success = register(username, password, role)

        if success:
            print("✅ Registration successful!")  # Debugging message
            return redirect(url_for('login_route'))
        else:
            print("❌ Registration failed!")
            return "Registration failed. Check the logs.", 500

    return render_template('register.html')


@app.route('/uploads', methods=['GET', 'POST'])
def uploads_page():
    username = session.get('username')  
    if not username:
        return redirect(url_for('login_route'))  

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        amount = request.form.get('amount')
        product_type = request.form.get('product_type')

        file = request.files.get('file')

        if not name or not file or not amount:
            return "Item Name, Image, and Price are required!", 400

        user_id = get_user_id(username)
        if not user_id:
            return "User not found!", 404

        filename = secure_filename(file.filename)
        file_path = f"static/uploads/{filename}"  
        file.save(file_path)
        insert_product(user_id, name, product_type, description, amount, file_path)



    # ✅ Fetch user's uploaded products
    user_id = get_user_id(username)  # Get user_id instead of username
    user_products = get_user_products(user_id)

    print("Fetched Products:", user_products)  # Debugging print

    return render_template('uploads.html', user_products=user_products)




@app.route('/upload', methods=['POST'])
def upload_item():
    filename = handle_upload()
    
    if isinstance(filename, tuple):  # If handle_upload() returns an error
        return filename

    return redirect(url_for('uploads_page'))

# ✅ Route to serve uploaded images correctly
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

#product page item single page 
@app.route('/product/<int:product_id>')
def single_item(product_id):
    product = get_product_by_id(product_id)
    print(product)  # ✅ Debugging: Check if seller_name appears now
    if not product:
        return "Product not found", 404
    
    return render_template('single_item.html', product=product)  # ✅ Pass single product

#seller page single item
@app.route('/seller_single_item/<int:product_id>')
def seller_single_item(product_id):
    # Fetch product details based on product_id
    product = get_product_by_id(product_id)  # Ensure this function exists
    if not product:
        return "Product not found", 404

    return render_template('seller_single_item.html', product=product)


@app.route('/start_auction/<int:product_id>', methods=['POST'])
def start_auction(product_id):
    # Fetch product details from the database
    product=get_product_details(product_id)
    
    if not product:
        return "Product not found!", 404

    product_name = product['product_name']
    initial_amount = product['amount']

    # Register for auction
    result = register_product_for_auction(product_id, product_name, initial_amount)
    flash("Item successfully registered for auction!")
    return redirect(url_for('seller_single_item', product_id=product_id))


@app.route('/edit_product/<int:product_id>')
def edit_product(product_id):
    # Logic for editing product
    return f"Edit page for product {product_id}"

@app.route('/admin')
def admin_page():
    return render_template('administrator.html')  # ✅ Show admin dashboard

#SHOW ALL PRODUCTS Of USERS
@app.route('/products')
def products_page():
    products = get_all_user_products()
    #print(products)  # ✅ Check if seller_name exists in the output
    return render_template('products.html', products=products)
@app.route('/products')
def products():
    product_type = request.args.get('product_type')

    if product_type:
        query = """
            SELECT p.product_id, p.product_name, p.description, p.amount, p.image_path, u.username AS seller_name
            FROM products p
            JOIN users u ON p.user_id = u.id
            WHERE p.type = %s
        """
        values = (product_type,)
    else:
        query = """
            SELECT p.product_id, p.product_name, p.description, p.amount, p.image_path, u.username AS seller_name
            FROM products p
            JOIN users u ON p.user_id = u.id
        """
        values = ()

    conn = getConnection()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, values)
    products = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('products.html', products=products)


# @app.route('/products')
# def products():
#     products = get_all_products()
#     return render_template("products.html", products=products)


@app.route('/test_redirect')
def test_redirect():
    return redirect(url_for('index'))


@app.route('/leaderboard')
def leaderboard():
    leaderboard_data = get_leaderboard_data()
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

@app.route('/bids/<int:product_id>')
def bids_page(product_id):
    return render_template("bids.html", product_id=product_id)


@app.route('/place_bid/<int:product_id>', methods=['GET', 'POST'])
def place_bid(product_id):
    username = session.get('username') 
    user_id = get_user_id(username)

    if not session.get("role") == "customer":
        return jsonify({"error": "Only customers can place a bid!"}), 403

    product = get_bids_product_details(product_id)
    if not product:
        return jsonify({"error": "Product not found!"}), 404

    if request.method == "POST":
        bid_amount = request.form.get("bid_amount")

        if not bid_amount:
            return jsonify({"error": "Bid amount is required!"}), 400

        try:
            bid_amount = float(bid_amount)
        except ValueError:
            return jsonify({"error": "Invalid bid amount!"}), 400

        # ✅ Call only once
        result = place_bid_query(product_id, user_id, bid_amount)

        if "error" in result:
            return jsonify(result), 400

        # ✅ Redirect to success page
        return redirect(url_for("bid_success", product_id=product_id))

    return render_template("bids.html", product=product, product_id=product_id)

@app.route('/bid_success/<int:product_id>')
def bid_success(product_id):
    product = get_bids_product_details(product_id)
    if not product:
        return jsonify({"error": "Product not found!"}), 404

    # Ensure product_id is always part of the product dict
    product["product_id"] = product_id

    return render_template("bid_success.html", product=product)

@app.route('/manage-users',methods=['GET', 'POST'])
def manage_users():
    myconn = getConnection()
    mycursor = myconn.cursor(dictionary=True)
    mycursor.execute("SELECT id, username, role FROM users")
    users = mycursor.fetchall()
    mycursor.close()
    myconn.close()
    return render_template("manage_users.html", users=users)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = get_user_by_id(user_id)  # your custom function to fetch user by ID

    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        update_user(user_id, username, role)  # your custom function to update user
        return redirect(url_for('manage_users'))

    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    myconn = getConnection()
    mycursor = myconn.cursor()
    query = "DELETE FROM users WHERE id = %s"
    mycursor.execute(query, (user_id,))
    myconn.commit()
    mycursor.close()
    myconn.close()
    return redirect(url_for('manage_users'))

@app.route('/Leaderboard-setting')
def leaderboard_settings():
    auctions = get_all_auctions()
    return render_template('leaderboard_settings.html',auctions=auctions)

@app.route('/reset-auctions', methods=['POST'])
def reset_auctions():
    # call your reset auction logic here
    reset_auction_data()

    flash("Auctions reset successfully!", "success")
    return redirect(url_for('leaderboard_settings'))

@app.route('/reset-bids', methods=['POST'])
def reset_bids():
    # call your reset bids logic here
    reset_bid_count()

    flash("All bids cleared!", "success")
    return redirect(url_for('leaderboard_settings'))

@app.route('/delete-auction/<int:product_id>', methods=['POST'])
def delete_auction(product_id):
    delete_single_auction(product_id)
    flash(f"🗑 Auction for product ID {product_id} deleted!", "info")
    return redirect(url_for('leaderboard_settings'))
    

@app.route('/logout')
def logout():
    """Logs out the user by clearing the session."""
    session.pop('username', None)
    return redirect(url_for('login_route'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    #app.run(debug=True)





""" seesion in  login route"""