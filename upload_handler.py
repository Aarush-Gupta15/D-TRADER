import os
from flask import request, session
from werkzeug.utils import secure_filename
from models.create_users import insert_product, get_user_id  

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')  # ✅ Save inside `static/uploads/`

# ✅ Ensure the `static/uploads/` folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def handle_upload():
    """Handles file uploads, saves them in `static/uploads/`, and inserts into DB."""

    if request.method == 'POST':
        # ✅ Fetch username from session
        username = session.get('username')  
        if not username:
            return "❌ Login required!", 401

        # ✅ Fetch user role from session (Ensure only sellers can upload)
        role = session.get('role')
        if role != 'seller':
            return "❌ Only sellers are allowed to upload!", 403

        # ✅ Fetch user ID from the database
        user_id = get_user_id(username)
        if not user_id:
            return "❌ User not found in database!", 404

        # ✅ Extract product details from the form
        product_name = request.form.get('name')  # Required field
        description = request.form.get('description', '')  # Optional
        amount = request.form.get('amount')  # ✅ Price field

        if not product_name or not amount:
            return "❌ Product Name and Amount are required!", 400
        
        try:
            amount = float(amount)  # ✅ Ensure it's a valid number
        except ValueError:
            return "❌ Invalid amount format!", 400

        # ✅ Get the uploaded file
        if 'file' not in request.files:
            return "❌ No file part!", 400
        
        file = request.files['file']
        if file.filename == '':
            return "❌ No selected file!", 400

        # ✅ Secure and save file
        filename = secure_filename(file.filename)
        relative_path = os.path.join('static/uploads', filename)  # ✅ Store only relative path
        file_path = os.path.join(UPLOAD_FOLDER, filename)  # ✅ Save file physically
        file.save(file_path)

        if os.path.exists(file_path):
            print(f"✅ File saved successfully: {file_path}")
        else:
            print("❌ File was NOT saved properly!")
            return "❌ File upload failed!", 500

        # ✅ Insert product details into the database (use relative path)
        insert_product(user_id, product_name, description, amount, relative_path)

        return "✅ Upload successful!", 200  # ✅ Return success response
