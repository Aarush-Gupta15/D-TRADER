import os
from flask import request, session
from werkzeug.utils import secure_filename
from models.create_users import insert_product, get_user_id

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')

# Ensure uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def handle_upload():
    if request.method == 'POST':
        username = session.get('username')
        if not username:
            return "❌ Login required!", 401

        role = session.get('role')
        if role != 'seller':
            return "❌ Only sellers can upload!", 403

        user_id = get_user_id(username)
        if not user_id:
            return "❌ User not found in database!", 404

        # ✅ Get form data
        product_name = request.form.get('name')
        product_type = request.form.get('product_type')  # NEW FIELD
        description = request.form.get('description', '')
        amount = request.form.get('amount')

        if not product_name or not amount or not product_type:
            return "❌ Product Name, Type, and Amount are required!", 400

        try:
            amount = float(amount)
        except ValueError:
            return "❌ Invalid amount format!", 400

        if 'file' not in request.files:
            return "❌ No file part!", 400

        file = request.files['file']
        if file.filename == '':
            return "❌ No selected file!", 400

        filename = secure_filename(file.filename)
        relative_path = os.path.join('static/uploads', filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # ✅ Insert into database
        insert_product(user_id, product_name, product_type, description, amount, relative_path)

        return "✅ Upload successful!", 200
