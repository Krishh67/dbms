-- Drop existing tables if they exist
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;

-- Create orders table with essential columns
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(50) NOT NULL,
    table_number VARCHAR(10) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create order_items table with essential columns
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(20) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Update orders table structure
ALTER TABLE orders
ADD COLUMN contact VARCHAR(20) AFTER table_number,
MODIFY COLUMN order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
MODIFY COLUMN status VARCHAR(20) DEFAULT 'pending';

-- Make sure all required columns exist
ALTER TABLE orders
ADD COLUMN IF NOT EXISTS order_id INT PRIMARY KEY AUTO_INCREMENT,
ADD COLUMN IF NOT EXISTS user_id VARCHAR(50) NOT NULL,
ADD COLUMN IF NOT EXISTS table_number VARCHAR(10) NOT NULL,
ADD COLUMN IF NOT EXISTS payment_method VARCHAR(20) NOT NULL,
ADD COLUMN IF NOT EXISTS special_instructions TEXT,
ADD COLUMN IF NOT EXISTS subtotal DECIMAL(10,2) NOT NULL,
ADD COLUMN IF NOT EXISTS tax DECIMAL(10,2) NOT NULL,
ADD COLUMN IF NOT EXISTS total DECIMAL(10,2) NOT NULL,
ADD COLUMN IF NOT EXISTS chef_id VARCHAR(50),
ADD COLUMN IF NOT EXISTS cooking_start_time TIMESTAMP NULL,
ADD COLUMN IF NOT EXISTS cooking_end_time TIMESTAMP NULL; 