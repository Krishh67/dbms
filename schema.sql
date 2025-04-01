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




























CREATE DATABASE dbms;
USE dbms;

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    item VARCHAR(100),
    price DECIMAL(10, 2)
);
show databases
use dbms;
show tables;

Create table canteen(
	name VARCHAR(100),
    img_url varchar(800),
    diet varchar(50));
    
    
ALTER TABLE canteen
ADD COLUMN ingredients TEXT,
ADD COLUMN prep_time INT,
ADD COLUMN cook_time INT,
ADD COLUMN flavor_profile VARCHAR(100),
ADD COLUMN course VARCHAR(100),
ADD COLUMN state VARCHAR(100),
ADD COLUMN region VARCHAR(100);
DESCRIBE canteen;


SET GLOBAL local_infile = 1;
LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Ifood_new.csv' 
INTO TABLE canteen
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS; -- If your CSV has a header

SHOW VARIABLES LIKE 'secure_file_priv';
select * from canteen









-- inserted user info
CREATE DATABASE dbms;
USE dbms;

CREATE TABLE users (
    user_id VARCHAR(10) PRIMARY KEY,
    sap_id BIGINT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(100) NOT NULL
);



INSERT INTO users (user_id, sap_id, full_name, password_hash) VALUES
('A059', 70562200012, 'GOSAVI, SHREYA', SHA2('pass', 256)),
('A061', 70562200014, 'MALHOTRA, JIYA', SHA2('pass', 256)),
('A080', 70562200041, 'KHETRE, OM', SHA2('pass', 256)),
('A086', 70562200049, 'SOLANKI, ARYAN', SHA2('pass', 256)),
('A091', 70562200061, 'MEHTA, KATHAN', SHA2('pass', 256)),
('A111', 70562300002, 'MISHRA, PARANTEY', SHA2('pass', 256)),
('A112', 70562300005, 'DHUMAL, MANAS', SHA2('pass', 256)),
('A113', 70562300007, 'GHARAT, SANIYA', SHA2('pass', 256)),
('A114', 70562300008, 'DEEPAK, PRATHAM', SHA2('pass', 256)),
('A115', 70562300009, 'JOSHI, BHAVYA', SHA2('pass', 256)),
('A116', 70562300010, 'MOTIWALA, ZAINAB', SHA2('pass', 256)),
('A117', 70562300011, 'FERNANDES, TAVIS', SHA2('pass', 256)),
('A118', 70562300012, 'JOGDAND, ADITYA', SHA2('pass', 256)),
('A119', 70562300015, 'GUPTA, ARYANMAN', SHA2('pass', 256)),
('A120', 70562300022, 'KALEEM, MOHD TABISH', SHA2('pass', 256)),
('A121', 70562300023, 'JAISWAL, SOUMIL', SHA2('pass', 256)),
('A122', 70562300024, 'AGARWAL, EKTA', SHA2('pass', 256)),
('A123', 70562300025, 'NIGADE, KARAN', SHA2('pass', 256)),
('A124', 70562300026, 'SHUKLA, ABHEDYA', SHA2('pass', 256)),
('A125', 70562300034, 'SARAF, SURYANSH', SHA2('pass', 256)),
('A126', 70562300035, 'GAJENDRA, LISHANG', SHA2('pass', 256)),
('A127', 70562300036, 'PATIL, MOHIT', SHA2('pass', 256)),
('A128', 70562300037, 'SARATHE, NISHANT', SHA2('pass', 256)),
('A129', 70562300039, 'HANDE, SOHAM', SHA2('pass', 256)),
('A131', 70562300041, 'KADAV, AADISHREE', SHA2('pass', 256)),
('A132', 70562300042, 'CHANDALURI, LEENA MAYUKHA', SHA2('pass', 256)),
('A134', 70562300044, 'SHAH, VIDHI', SHA2('pass', 256)),
('A135', 70562300045, 'DEDHIA, MANAN', SHA2('pass', 256)),
('A136', 70562300046, 'SOHNI, VINAYAK', SHA2('pass', 256)),
('A137', 70562300047, 'SHITOLE, TANVI', SHA2('pass', 256)),
('A138', 70562300048, 'PRAKASH, SANJEEV', SHA2('pass', 256)),
('A139', 70562300049, 'SAWANT, MAYANK', SHA2('pass', 256)),
('A143', 70562300059, 'SHANKLESHA, KRIYA', SHA2('pass', 256)),
('A144', 70562300060, '., LAVANYA', SHA2('pass', 256)),
('A145', 70562300061, 'JAIN, LUCKY', SHA2('pass', 256)),
('A146', 70562300062, 'PATIL, RAHUL', SHA2('pass', 256)),
('A147', 70562300063, 'RANI, SHRUTI', SHA2('pass', 256)),
('A149', 70562300065, 'SHAIKH, FAMIDA', SHA2('pass', 256)),
('A150', 70562300066, 'MAHAPATRO, MEET', SHA2('pass', 256)),
('A151', 70562300067, 'JADHAV, VREHA', SHA2('pass', 256)),
('A152', 70562300071, 'TURALKAR, ARYAN', SHA2('pass', 256)),
('A153', 70562300072, 'PONDA, DIYA', SHA2('pass', 256)),
('A154', 70562300073, 'PATEL, KRISH', SHA2('pass', 256)),
('A155', 70562300074, 'HULE, PARTH', SHA2('pass', 256)),
('A156', 70562300075, 'SEERVI, NIKITA', SHA2('pass', 256)),
('A157', 70562300076, 'KHABALE, AARYA', SHA2('pass', 256)),
('A159', 70562300078, 'SHAKTHIVEL, RATESHWARI', SHA2('pass', 256)),
('A160', 70562300079, 'VINCHU, SNEHA', SHA2('pass', 256)),
('A161', 70562300091, 'MULCHANDANI, DISHA', SHA2('pass', 256)),
('A162', 70562300092, 'VIRDI, SANVEER SINGH', SHA2('pass', 256)),
('A163', 70562300093, 'PATIL, BHAGYASHREE', SHA2('pass', 256)),
('A167', 70562300100, 'KOHLI, ARYAN', SHA2('pass', 256)),
('A168', 70562300102, 'SAMRADNYI, KALE', SHA2('pass', 256)),
('A169', 70562300103, 'GULVE, ARNAV', SHA2('pass', 256)),
('A170', 70562300105, 'PANDEY, VAIBHAV', SHA2('pass', 256)),
('A171', 70562300106, 'DHUMAL, OM', SHA2('pass', 256)),
('A172', 70562300108, 'RAJAK, SHRUTI', SHA2('pass', 256)),
('A173', 70562300109, 'MARAKKAR, SHAZEEN', SHA2('pass', 256)),
('A174', 70562400169, 'MOHAMMADMUZAMILL, SAUDAGAR', SHA2('pass', 256)),
('A175', 70562400170, 'AADIBMALIM, MALIM', SHA2('pass', 256)),
('A176', 70562400171, 'PRADNYA, GOKHALE', SHA2('pass', 256)),
('A177', 70562400172, 'ANMOL, SHAH', SHA2('pass', 256)),
('A220', 70022300270, 'P Venkata Sagar Siddhartha', SHA2('pass', 256));

use root;
SELECT * FROM users;

show tables;
-- modified cart canteen
create table cart
select * from canteen;

ALTER TABLE canteen
ADD COLUMN item_id INT AUTO_INCREMENT PRIMARY KEY;

ALTER TABLE canteen
ADD COLUMN price DECIMAL(10, 2) NOT NULL;
SET SQL_SAFE_UPDATES = 0;
UPDATE canteen
SET price = FLOOR(150 + (RAND() * (350 - 100)))
WHERE item_id IS NOT NULL;  -- Ensure you're updating rows where item_id is present (or any other condition)

-- Modify menu table



ALTER TABLE canteen 
MODIFY COLUMN item_id INT AUTO_INCREMENT,
ADD COLUMN category1 VARCHAR(50) DEFAULT 'menu';
-- created drinks tabel 
use dbms;
CREATE TABLE drinks (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    img_url VARCHAR(255),
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample drinks with actual image URLs
INSERT INTO drinks (name, description, price, img_url, category) VALUES
('Fresh Orange Juice', 'Freshly squeezed orange juice', 99.00, 'https://media.istockphoto.com/photos/fresh-orange-juice-and-fruit-on-wooden-table-picture-id1174799227', 'Juice'),
('Coffee', 'Premium blend coffee', 79.00, 'https://media.istockphoto.com/photos/fresh-coffee-on-dark-background-picture-id1280291834', 'Hot Beverages'),
('Fruit Smoothie', 'Fruit smoothie with yogurt', 129.00, 'https://media.istockphoto.com/photos/fresh-fruit-smoothie-with-banana-and-strawberry-picture-id1286536360', 'Smoothies');




ALTER TABLE drinks 
MODIFY COLUMN item_id INT AUTO_INCREMENT,
ADD COLUMN category VARCHAR(50) DEFAULT 'drinks';


select * from drinks

-- created cart table 
CREATE TABLE cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,  -- Primary Key
    user_id VARCHAR(10),  -- Foreign Key referencing users
    item_id INT,  -- Foreign Key referencing canteen
    quantity INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (item_id) REFERENCES canteen(item_id)
);

select * from cart
TRUNCATE TABLE cart;

ALTER TABLE cart 
ADD COLUMN item_name VARCHAR(100);


ALTER TABLE cart 
ADD COLUMN category1 VARCHAR(50),
ADD UNIQUE KEY unique_cart_item_category (user_id, item_id, category1);






-- Create the 'meals' table


-- Drop the table if it exists
DROP TABLE IF EXISTS orders;

-- Create the 'meals' table
CREATE TABLE meals (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    image_url VARCHAR(255),
    category1 VARCHAR(50) DEFAULT 'meals' -- Set default value to 'meals'
);

-- Insert sample records with 'category1' set to 'meals'
INSERT INTO meals (item_name, price, description, category, category1) VALUES
('Paneer Tikka', 200.00, 'Grilled cottage cheese with spices', 'Appetizer', 'meals'),
('Naan', 40.00, 'Fresh baked Indian bread', 'Bread', 'meals'),
('Biryani', 300.00, 'Fragrant rice with spices', 'Main Course', 'meals');

-- Query to see the records in the meals table
SELECT * FROM canteen;
