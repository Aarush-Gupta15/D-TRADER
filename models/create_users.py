import mysql.connector
def getConnection():
    global myconn
    myconn = mysql.connector.connect(host="localhost",user="root",password="",database="D_TRADE")

    if myconn.is_connected():
        return myconn
    #print("Connected to MySQL successfully!")

#myconn.close()
def login(username, password):
    getConnection()  # Ensure MySQL connection
    mycursor = myconn.cursor(dictionary=True)

    # ✅ Use the correct column name: `password_hash`
    mysqlquery = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
    mycursor.execute(mysqlquery, (username, password))
    user = mycursor.fetchone()  # Fetch user if exists

    mycursor.close()

    print(f"Database Query Result: {user}")  # Debugging print

    return user  # Returns user record if found, else None

def get_user_by_id(user_id):
    myconn = getConnection()
    mycursor = myconn.cursor(dictionary=True)

    try:
        query = "SELECT id, username, role FROM users WHERE id = %s"
        mycursor.execute(query, (user_id,))
        user = mycursor.fetchone()
        return user  # This will be a dictionary or None if not found
    except Exception as e:
        print("Error fetching user by ID:", e)
        return None
    finally:
        mycursor.close()
        myconn.close()

def register(username, password, role):
    """Registers a new user with a specified role."""
    getConnection()  # Ensure `myconn` is initialized

    if myconn is None:
        print("❌ Database connection failed.")
        return False

    # ✅ Ensure only allowed roles are stored
    if role not in ["admin_user", "seller", "customer"]:
        print(f"❌ Invalid role: {role}")
        return False

    try:
        mycursor = myconn.cursor()
        print(f"Registering User: {username}, Password: {password}, Role: {role}")  # Debug print

        mysqlquery = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"
        values = (username, password, role)
        mycursor.execute(mysqlquery, values)
        myconn.commit()
        mycursor.close()
        
        print(f"✅ User '{username}' registered successfully as '{role}'")
        return True
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        return False
#register("bu","1234","user")


# Function to insert product details into DB
def insert_product(user_id, product_name, product_type, description, amount, image_path):
    getConnection()
    mycursor = myconn.cursor()

    mysqlquery = """
    INSERT INTO products (user_id, product_name, type, description, amount, image_path)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (user_id, product_name, product_type, description, amount, image_path)

    try:
        mycursor.execute(mysqlquery, values)
        myconn.commit()
        print("✅ Product inserted successfully!")
    except Exception as e:
        print(f"❌ Error inserting product: {e}")
    finally:
        mycursor.close()
        myconn.close()


def update_user(user_id, username, role):
    myconn = getConnection()
    mycursor = myconn.cursor()
    query = "UPDATE users SET username = %s, role = %s WHERE id = %s"
    mycursor.execute(query, (username, role, user_id))
    myconn.commit()
    mycursor.close()
    myconn.close()
    


# Function to get all products
def get_all_products():
    getConnection()
    mycursor = myconn.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM products")
    items = mycursor.fetchall()
    mycursor.close()
    myconn.close()
    return items

def get_user_id(username):
    getConnection()
    """Fetches user ID from the database using the username."""
    mycursor = myconn.cursor(dictionary=True)

    mysqlquery = "SELECT id FROM users WHERE username = %s"
    values = (username,)  # ✅ Correct tuple format

    mycursor.execute(mysqlquery, values)
    user = mycursor.fetchone()

    mycursor.close()
    myconn.close()

    #print(user)
    return user["id"] if user else None  # ✅ Return user ID if found

#get_user_id('E23CSEU0008')
# def insert_product(user_id, product_name, description, amount, image_path):
#     getConnection()
#     mycursor = myconn.cursor()

#     mysqlquery = """
#         INSERT INTO products (user_id, product_name, description, amount, image_path) 
#         VALUES (%s, %s, %s, %s, %s)
#     """
#     values = (user_id, product_name, description, amount, image_path)

#     try:
#         mycursor.execute(mysqlquery, values)
#         myconn.commit()
#         print("✅ Product inserted successfully!")
#     except mysql.connector.Error as err:
#         print(f"❌ Error inserting product: {err}")
#     finally:
#         mycursor.close()
#         myconn.close()

def get_user_products(user_id):
    getConnection()  # Ensure connection is established
    mycursor = myconn.cursor(dictionary=True)

    mysqlquery = """
        SELECT p.product_id, p.product_name, p.description, p.amount, p.image_path, u.username AS seller_name
        FROM products p
        JOIN users u ON p.user_id = u.id
        WHERE p.user_id = %s  -- ✅ Fetch only products for the given user
    """

    mycursor.execute(mysqlquery, (user_id,))
    products = mycursor.fetchall()

    mycursor.close()
    myconn.close()
    
    return products  # ✅ Ensure product_id is included in the result

def get_all_users():
    getConnection()

    mycursor = myconn.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM users")
    user= mycursor.fetchall()
    mycursor.close()
    myconn.close()
    return user


def get_all_user_products():
    getConnection()  # Make sure the connection is initialized

    if myconn is None:
        print("Database connection failed")
        return []

    with myconn.cursor(dictionary=True) as mycursor:
        mysqlquery = """
            SELECT p.product_id, p.product_name, p.description, p.amount, p.image_path, u.username AS seller_name
            FROM products p
            JOIN users u ON p.user_id = u.id  -- ✅ Join users table to fetch username
        """

        mycursor.execute(mysqlquery)
        products = mycursor.fetchall()  # ✅ Fetch all products

    myconn.close()  # ✅ Close connection after query execution
    return products  # ✅ Return products

    
    return products  # ✅ Ensure this returns the seller_name

def single_item_product(product_id):
    """Fetch a single product by its ID from the database."""
    getConnection()
    try:
        mycursor = myconn.cursor(dictionary=True)  # ✅ Fetch results as dictionaries
        mycursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = mycursor.fetchone()  # ✅ Fetch ONE product, NOT a list
        return product  # ✅ Return the product dictionary
    except Exception as e:
        print("Error fetching product:", e)
        return None
    finally:
        mycursor.close()  # ✅ Close cursor after operation

def get_product_by_id(product_id):
    getConnection()
    mycursor = myconn.cursor(dictionary=True)

   
    mysqlquery = """
        SELECT p.product_id, p.product_name, p.description, p.amount, p.image_path, u.username AS seller_name
        FROM products p
        JOIN users u ON p.user_id = u.id  -- ✅ Ensure proper join with users
        WHERE p.product_id = %s
    """

    
    mycursor.execute(mysqlquery, (product_id,))
    product = mycursor.fetchone()  # Fetch a single product

    mycursor.close()
    myconn.close()

    return product  # Returns None if not found

def place_bid(auction_id, bid_amount):
    getConnection()
    mycursor = myconn.cursor(dictionary=True)

    # Get current bid count
    mycursor.execute("SELECT bid_count, highest_bid FROM auction WHERE auction_id = %s", (auction_id,))
    auction = mycursor.fetchone()
    
    if not auction:
        return "Auction not found!"
    
    if auction['bid_count'] >= 5:
        return "Bidding limit reached! No more bids allowed."

    if bid_amount <= auction['highest_bid']:
        return "Your bid must be higher than the current highest bid."

    # Update auction with new bid
    mysqlquery = """
        UPDATE auction
        SET highest_bid = %s, bid_count = bid_count + 1
        WHERE auction_id = %s
    """
    mycursor.execute(mysqlquery, (bid_amount, auction_id))
    myconn.commit()
    
    mycursor.close()
    myconn.close()

    return "Bid placed successfully!"

#auction

def register_product_for_auction(product_id, product_name, initial_amount):
    getConnection()
    mycursor = myconn.cursor()

    query = """
        INSERT INTO auction (product_id, product_name, initial_amount, bid_count, highest_bid)
        VALUES (%s, %s, %s, 0, %s)
    """

    try:
        mycursor.execute(query, (product_id, product_name, initial_amount, initial_amount))
        myconn.commit()
    except mysql.connector.IntegrityError:
        return "This product is already registered for auction!"
    finally:
        mycursor.close()
        myconn.close()

    return "Product registered for auction successfully!"


def place_bid(product_id, bid_amount):
    getConnection()
    mycursor = myconn.cursor()

    # Check current bid count
    mycursor.execute("SELECT bid_count FROM auction WHERE product_id = %s", (product_id,))
    result = mycursor.fetchone()
    
    if result and result['bid_count'] >= 5:
        return "Bidding limit reached!", 400  # Prevent further bids
    
    # Place the bid
    query = """
        UPDATE auction 
        SET highest_bid = %s, bid_count = bid_count + 1
        WHERE product_id = %s AND bid_count < 5
    """
    mycursor.execute(query, (bid_amount, product_id))
    myconn.commit()
    mycursor.close()
    myconn.close()

    return "Bid placed successfully!"

def get_product_details(product_id):
    """Fetch product name and amount for a given product_id."""
    getConnection()  # Ensure the database connection is established
    mycursor = myconn.cursor(dictionary=True)

    mysql_query = "SELECT product_name, amount FROM products WHERE product_id = %s"
    mycursor.execute(mysql_query, (product_id,))
    product = mycursor.fetchone()

    mycursor.close()
    myconn.close()

    return product  # Returns a dictionary with product details

#reset auction data
def reset_auction_data():

    getConnection()  
    mycursor = myconn.cursor()
    
    mycursor.execute("TRUNCATE TABLE auction")  # Reset auction table
    myconn.commit()
    
    mycursor.close()
    myconn.close()

#leaderboard page

def get_leaderboard_data():
    """Fetches top 5 products with highest bids along with seller details."""
    myconn = getConnection()
    mycursor = myconn.cursor(dictionary=True)

    mysqlquery = """
        SELECT 
            a.product_id, 
            a.product_name, 
            a.initial_amount, 
            a.highest_bid, 
            p.image_path AS product_image, 
            u.username AS seller_name
        FROM auction a
        JOIN products p ON a.product_id = p.product_id
        JOIN users u ON p.user_id = u.id
        ORDER BY a.highest_bid DESC
        LIMIT 5;
    """
    
    mycursor.execute(mysqlquery)
    leaderboard_data = mycursor.fetchall()

    mycursor.close()
    myconn.close()
    
    return leaderboard_data

def place_bid_query(product_id, user_id, bid_amount):
    myconn = getConnection()
    mycursor = myconn.cursor(dictionary=True)

    try:
        # ✅ Get the current highest bid
        mycursor.execute("SELECT highest_bid FROM auction WHERE product_id = %s", (product_id,))
        auction = mycursor.fetchone()

        if not auction:
            return {"error": "Auction not found!"}

        highest_bid = auction["highest_bid"]

         #❌ If bid is not higher
        if bid_amount <= highest_bid:
             return {"error": "Bid must be higher than the current highest bid!"}

        # ✅ 1. Insert into bids table
        insert_bid = """
            INSERT INTO bids (product_id, user_id, bid_amount)
            VALUES (%s, %s, %s)
        """
        mycursor.execute(insert_bid, (product_id, user_id, bid_amount))

        # ✅ 2. Update auction table
        update_auction = """
            UPDATE auction 
            SET highest_bid = %s, bid_count = bid_count + 1
            WHERE product_id = %s
        """
        mycursor.execute(update_auction, (bid_amount, product_id))

        myconn.commit()
        return {"message": "✅ Bid placed successfully!"}

    except mysql.connector.Error as err:
        return {"error": str(err)}

    finally:
        mycursor.close()
        myconn.close()



def get_bids_product_details(product_id):
    """
    Fetch product details including name, description, image, and seller name.
    """
    query = """
    SELECT p.product_name, p.description, p.image_path, u.username AS seller_name
    FROM products p
    JOIN users u ON p.user_id = u.id  -- ✅ Corrected: 'u.id' instead of 'u.user_id'
    WHERE p.product_id = %s
    """
    myconn = getConnection()
    mycursor = myconn.cursor(dictionary=True)
    mycursor.execute(query, (product_id,))
    product = mycursor.fetchone()
    mycursor.close()
    myconn.close()
    
    return product  # Returns None if product doesn't exist

def get_all_bids_with_users():
    myconn = getConnection()
    mycursor = myconn.cursor(dictionary=True)

    query = """
    SELECT 
        b.bid_id,
        b.product_id,
        p.product_name,
        p.amount AS initial_amount,
        b.bid_amount AS highest_bid,
        c.username AS customer_name, 
        s.username AS seller_name
    FROM bids b
    JOIN products p ON b.product_id = p.product_id
    JOIN users c ON b.user_id = c.id  -- Fetch customer name
    JOIN users s ON p.user_id = s.id; -- Fetch seller name
    """
    
    mycursor.execute(query)
    bids = mycursor.fetchall()

    mycursor.close()
    myconn.close()
    
    return bids

def reset_bid_count():
    myconn = getConnection()
    mycursor = myconn.cursor()

    try:
        query = "UPDATE auction SET bid_count = 0"
        mycursor.execute(query)
        myconn.commit()
        print("✅ All bid counts have been reset to 0.")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    
    finally:
        mycursor.close()
        myconn.close()

def get_all_auctions():
    myconn = getConnection()
    mycursor = myconn.cursor(dictionary=True)

    query = """
        SELECT a.product_id, a.product_name, a.initial_amount, a.highest_bid, a.bid_count, p.image_path
        FROM auction a
        JOIN products p ON a.product_id = p.product_id
    """
    mycursor.execute(query)
    auctions = mycursor.fetchall()

    mycursor.close()
    myconn.close()
    return auctions

def delete_single_auction(product_id):
    myconn = getConnection()
    mycursor = myconn.cursor()

    try:
        mycursor.execute("DELETE FROM auction WHERE product_id = %s", (product_id,))
        myconn.commit()
    except Exception as e:
        print(f"❌ Error deleting auction: {e}")
    finally:
        mycursor.close()
        myconn.close()
