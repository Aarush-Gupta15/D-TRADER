import os
import mysql.connector
from models.create_users import getConnection

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')

def reset_all_data():
    try:
        myconn = getConnection()
        mycursor = myconn.cursor()

        # Step 1: Delete from child to parent (order matters!)
        mycursor.execute("DELETE FROM bids")
        mycursor.execute("DELETE FROM auction")
        mycursor.execute("DELETE FROM products")
        mycursor.execute("DELETE FROM users")
        myconn.commit()
        print("✅ All table data deleted.")

        # Step 2: Reset AUTO_INCREMENT values
        mycursor.execute("ALTER TABLE bids AUTO_INCREMENT = 1")
        mycursor.execute("ALTER TABLE auction AUTO_INCREMENT = 1")
        mycursor.execute("ALTER TABLE products AUTO_INCREMENT = 1")
        mycursor.execute("ALTER TABLE users AUTO_INCREMENT = 1")
        myconn.commit()
        print("🔄 AUTO_INCREMENT counters reset.")

        # Step 3: Delete all uploaded images
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"🗑 Deleted image: {file_path}")

        mycursor.close()
        myconn.close()
        print("🎉 Reset complete.")

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")

if __name__ == "__main__":
    reset_all_data()
