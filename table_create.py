import mysql.connector

def create_database_and_tables():
    # Connect to MySQL server (no specific database yet)
    myconn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    mycursor = myconn.cursor()

    # ✅ Create Database
    mycursor.execute("CREATE DATABASE IF NOT EXISTS D_TRADE")
    print("✅ Database D_TRADE created or already exists.")

    # ✅ Use the newly created database
    mycursor.execute("USE D_TRADE")

    # ✅ Create users table
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            password_hash VARCHAR(128) NOT NULL,
            role ENUM('admin_user', 'seller', 'customer') NOT NULL DEFAULT 'customer'
        )
    """)
    print("✅ users table created.")

    # ✅ Trigger to allow only one admin_user
    mycursor.execute("DROP TRIGGER IF EXISTS prevent_multiple_admins")
    mycursor.execute("""
        CREATE TRIGGER prevent_multiple_admins
        BEFORE INSERT ON users
        FOR EACH ROW
        BEGIN
            IF NEW.role = 'admin_user' AND (SELECT COUNT(*) FROM users WHERE role = 'admin_user') >= 1 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Only one admin is allowed!';
            END IF;
        END;
    """)
    print("✅ Trigger added to restrict admin_user.")

    # ✅ Create products table
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            product_name VARCHAR(255) NOT NULL,
            type VARCHAR(100) NOT NULL,
            description TEXT,
            amount DECIMAL(10,2) NOT NULL,
            image_path VARCHAR(255) NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    print("✅ products table created.")

    # ✅ Create auction table
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS auction (
            auction_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT UNIQUE NOT NULL,
            product_name VARCHAR(255) NOT NULL,
            initial_amount DECIMAL(10,2) NOT NULL,
            bid_count INT DEFAULT 0 CHECK (bid_count <= 5),
            highest_bid DECIMAL(10,2) DEFAULT 0.00,
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
        )
    """)
    print("✅ auction table created.")

    # ✅ Create bids table
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS bids (
            bid_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL,
            user_id INT NOT NULL,
            bid_amount DECIMAL(10,2) NOT NULL,
            bid_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    print("✅ bids table created.")

    # ✅ Insert default admin_user if not already present
    mycursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin_user'")
    if mycursor.fetchone()[0] == 0:
        mycursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (%s, %s, %s)
        """, ("admin_user", "1234", "admin_user"))
        print("✅ Default admin_user inserted.")

    # ✅ Commit changes and close connection
    myconn.commit()
    mycursor.close()
    myconn.close()
    print("✅ All tables created and default admin_user set.")


# ✅ Run the function
if __name__ == "__main__":
    create_database_and_tables()
