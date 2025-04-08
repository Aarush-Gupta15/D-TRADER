CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role ENUM('admin_user', 'seller', 'customer') NOT NULL DEFAULT 'customer'
);

-- Ensure only ONE admin exists
DELIMITER //
CREATE TRIGGER prevent_multiple_admins
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    IF NEW.role = 'admin' AND (SELECT COUNT(*) FROM users WHERE role = 'admin') >= 1 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Only one admin is allowed!';
    END IF;
END;
//
DELIMITER ;
-- product table

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    amount DECIMAL(10,2) NOT NULL,  -- ✅ Added Amount Column
    image_path VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- auction table;
CREATE TABLE auction (
    auction_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    initial_amount DECIMAL(10,2) NOT NULL,
    bid_count INT DEFAULT 0 CHECK (bid_count <= 5),  -- ✅ Restricts max bids to 5
    highest_bid DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);



