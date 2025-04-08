import os
from models.create_users import getConnection, reset_bid_count

# ✅ Get the MySQL connection
myconn = getConnection()
mycursor = myconn.cursor()

# ✅ Fetch all image paths before deleting records
mycursor.execute("SELECT image_path FROM products")
image_paths = mycursor.fetchall()

# ✅ Delete all records from `products` table (use DELETE, not TRUNCATE)
mycursor.execute("DELETE FROM products")
myconn.commit()

# ✅ Delete images from `static/uploads/` directory
for (path,) in image_paths:
    if os.path.exists(path):
        os.remove(path)
        print(f"🗑 Deleted: {path}")

# ✅ Close connections
mycursor.close()
myconn.close()
print("✅ Database & Images Deleted Successfully!")

reset_bid_count()
print("BIDS ARE RESET")
