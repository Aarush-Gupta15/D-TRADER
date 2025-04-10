-- Insert the Admin (Only one admin is allowed)
INSERT INTO users (username, password_hash, role) 
VALUES ('admin_user', '1515', 'admin');

-- Insert Sample Users
INSERT INTO users (username, password_hash, role) 
VALUES 
('user1', 'userpass1', 'user'),
('user2', 'userpass2', 'user'),
('user3', 'userpass3', 'user');

SELECT * FROM USERS;
-- drop table users; to delete table

INSERT INTO users (username, password_hash, role)
VALUES ('admin_user', '1234', 'admin_user');
