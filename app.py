from flask import Flask, render_template, request, session, redirect, url_for, flash,jsonify
import mysql.connector
import os
from decimal import Decimal
from datetime import datetime
app = Flask(__name__)

app.secret_key = 'dev_secret_key_change_in_production'
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="dbms"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None

def findname(user_id):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT full_name FROM users WHERE user_id = %s", 
            (user_id,)
        )
        result = cursor.fetchone()
        
        return result['full_name'] if result else None
    
    except mysql.connector.Error as err:
        print(f"Database Error in findname: {err}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def verify_login(user_id, password):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return False

        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE user_id = %s AND password_hash = SHA2(%s, 256)", 
            (user_id, password)
        )
        result = cursor.fetchone()
        
        return result is not None
    
    except mysql.connector.Error as err:
        print(f"Database Error in verify_login: {err}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if verify_login(username, password):
            session['username'] = username 
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    name = findname(session['username'])
    return render_template('home.html', name=name)

@app.route('/category/menu')
def menu2():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    name = findname(session['username'])
    return render_template('category/menu.html', name=name)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'dbms'
}

# Add this route to your app.py file
@app.route('/menu')
def get_menu():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Execute query to get all menu items
        cursor.execute("SELECT * FROM canteen")
        menu_items = cursor.fetchall()
        #print(menu_items,"checkuibnggggggggggggggggggggggggggggggggggg")
        # Check if menu_items is empty
        # Close connection
        cursor.close()
        conn.close()
        
        return jsonify(menu_items)
    except Exception as e:
        print(f"Error fetching menu data: {e}")
        return jsonify([]), 500



@app.route('/category/meals')
def meals():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch meals from the database
        cursor.execute("SELECT * FROM meals")
        meals_items = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        name = findname(session['username'])
        return render_template('category/meals.html', name=name, meals=meals_items)
    except Exception as e:
        print(f"Error fetching meals: {e}")
        flash('Could not load meals menu.', 'error')
        return render_template('category/meals.html', name=findname(session['username']), meals=[])

@app.route('/category/drinks')
def drinks():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch drinks from the database
        cursor.execute("SELECT * FROM drinks")
        drinks_items = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        name = findname(session['username'])
        return render_template('category/drinks.html', name=name, drinks=drinks_items)
    except Exception as e:
        print(f"Error fetching drinks: {e}")
        return render_template('category/drinks.html', name=findname(session['username']), drinks=[])

@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        print(f"Fetching cart items for user: {session['username']}")  # Debug log
        
        # First, let's check what's in the cart table directly
        cursor.execute("SELECT * FROM cart WHERE user_id = %s", (session['username'],))
        raw_cart_items = cursor.fetchall()
        print(f"Raw cart items: {raw_cart_items}")  # Debug log
        
        # Now fetch cart items with prices from their respective tables
        cursor.execute("""
            SELECT c.item_id, c.item_name, c.quantity, c.category1,
                   CASE 
                       WHEN c.category1 = 'drinks' THEN d.price
                       WHEN c.category1 = 'meals' THEN m.price
                       WHEN c.category1 = 'canteen' THEN canteen.price
                   END as price
            FROM cart c
            LEFT JOIN drinks d ON c.item_id = d.item_id AND c.category1 = 'drinks'
            LEFT JOIN meals m ON c.item_id = m.item_id AND c.category1 = 'meals'
            LEFT JOIN canteen ON c.item_id = canteen.item_id AND c.category1 = 'canteen'
            WHERE c.user_id = %s
        """, (session['username'],))
        
        cart_items = cursor.fetchall()
        print(f"Cart items with prices: {cart_items}")  # Debug log
        
        # Calculate totals
        subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
        tax = subtotal * 0.08  # 8% tax
        total = subtotal + tax
        
        cursor.close()
        conn.close()
        
        name = findname(session['username'])
        return render_template('add_to_cart.html', 
                             name=name, 
                             items=cart_items,
                             subtotal=subtotal,
                             tax=tax,
                             total=total)
    except Exception as e:
        print(f"Error fetching cart items: {e}")
        return render_template('add_to_cart.html', 
                             name=findname(session['username']), 
                             items=[],
                             subtotal=0,
                             tax=0,
                             total=0)

@app.route('/checkout')
def checkout():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch cart items with prices
        cursor.execute("""
            SELECT c.item_id, c.item_name, c.quantity, c.category1,
                   CASE 
                       WHEN c.category1 = 'drinks' THEN d.price
                       WHEN c.category1 = 'meals' THEN m.price
                       ELSE canteen.price
                   END as price
            FROM cart c
            LEFT JOIN drinks d ON c.item_id = d.item_id AND c.category1 = 'drinks'
            LEFT JOIN meals m ON c.item_id = m.item_id AND c.category1 = 'meals'
            LEFT JOIN canteen ON c.item_id = canteen.item_id AND c.category1 = 'canteen'
            WHERE c.user_id = %s
        """, (session['username'],))

        cart_items = cursor.fetchall()

        # Calculate totals
        subtotal = sum(Decimal(str(item['price'])) * Decimal(str(item['quantity'])) for item in cart_items)
        tax = subtotal * Decimal('0.08')  # 8% tax
        total = subtotal + tax

        cursor.close()
        conn.close()
        
        name = findname(session['username'])
        return render_template('checkout.html', 
                             name=name, 
                             items=cart_items,
                             subtotal=subtotal,
                             tax=tax,
                             total=total)
    except Exception as e:
        print(f"Error fetching checkout items: {e}")
        return redirect(url_for('cart'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        # Get form data
        item_id = request.form.get('item_id')
        quantity = int(request.form.get('quantity', 1))
        category = request.form.get('category')
        item_name = request.form.get('item_name')
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Check if item already exists in cart
        cursor.execute("""
            SELECT * FROM cart 
            WHERE user_id = %s AND item_id = %s AND category1 = %s
        """, (session['username'], item_id, category))
        existing_item = cursor.fetchone()

        if existing_item:
            # Update quantity if item exists
            cursor.execute("""
                UPDATE cart 
                SET quantity = quantity + %s 
                WHERE user_id = %s AND item_id = %s AND category1 = %s
            """, (quantity, session['username'], item_id, category))
        else:
            # Insert new item if it doesn't exist
            cursor.execute("""
                INSERT INTO cart (user_id, item_id, quantity, category1, item_name)
                VALUES (%s, %s, %s, %s, %s)
            """, (session['username'], item_id, quantity, category, item_name))

        conn.commit()
        cursor.close()
        conn.close()
            
        flash('Item added to cart successfully!', 'success')
    except Exception as e:
        print(f"Error adding to cart: {e}")
        flash('Error adding item to cart', 'error')
    
    # Redirect based on category
    if category == 'drinks':
        return redirect(url_for('drinks'))
    elif category == 'meals':
        return redirect(url_for('meals'))
    else:
        return redirect(url_for('menu2'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/process_payment', methods=['POST'])
def process_payment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        # Get form data
        table_number = request.form.get('table_number')
        contact = request.form.get('contact')
        payment_method = request.form.get('payment_method')
        special_instructions = request.form.get('special_instructions')
        upi_reference = request.form.get('upi_reference') if payment_method == 'upi' else None
        
        # Store payment details in session for later use
        session['payment_details'] = {
            'table_number': table_number,
            'contact': contact,
            'payment_method': payment_method,
            'special_instructions': special_instructions,
            'upi_reference': upi_reference
        }
        
        # Redirect to payment processing animation
        return redirect(url_for('payment_processing'))
        
    except Exception as e:
        print(f"Error processing payment: {e}")
        flash('Error processing payment. Please try again.', 'error')
        return redirect(url_for('checkout'))

@app.route('/payment_processing')
def payment_processing():
    if 'username' not in session or 'payment_details' not in session:
        return redirect(url_for('login'))
    return render_template('payment.html')

@app.route('/order_status/<int:order_id>')
def order_status(order_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get order details
        cursor.execute("""
            SELECT * FROM orders WHERE order_id = %s AND user_id = %s
        """, (order_id, session['username']))
        order = cursor.fetchone()
        
        if not order:
            flash('Order not found')
            return redirect(url_for('index'))
            
        # Get order items
        cursor.execute("""
            SELECT * FROM order_items
            WHERE order_id = %s
        """, (order_id,))
        order_items = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Ensure status is set
        if not order['status']:
            order['status'] = 'pending'
        
        return render_template('order_status.html', order=order, order_items=order_items)
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('An error occurred while fetching the order status')
        return redirect(url_for('index'))

@app.route('/complete_payment')
def complete_payment():
    if 'username' not in session or 'payment_details' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get cart items with their prices
        cursor.execute("""
            SELECT c.*, 
                   CASE 
                       WHEN c.category1 = 'drinks' THEN d.price
                       WHEN c.category1 = 'meals' THEN m.price
                       WHEN c.category1 = 'canteen' THEN canteen.price
                   END as price
            FROM cart c
            LEFT JOIN drinks d ON c.item_id = d.item_id AND c.category1 = 'drinks'
            LEFT JOIN meals m ON c.item_id = m.item_id AND c.category1 = 'meals'
            LEFT JOIN canteen ON c.item_id = canteen.item_id AND c.category1 = 'canteen'
            WHERE c.user_id = %s
        """, (session['username'],))
        cart_items = cursor.fetchall()
        
        if not cart_items:
            flash('Your cart is empty')
            return redirect(url_for('cart'))
        
        # Calculate total
        total_amount = sum(Decimal(str(item['price'])) * item['quantity'] for item in cart_items)
        
        # Get payment details from session
        payment_details = session['payment_details']
        
        # Create order record with simplified fields
        cursor.execute("""
            INSERT INTO orders (user_id, table_number, total_amount, status)
            VALUES (%s, %s, %s, 'pending')
        """, (
            session['username'],
            payment_details['table_number'],
            float(total_amount)
        ))
        order_id = cursor.lastrowid
        
        # Create order items records
        for item in cart_items:
            cursor.execute("""
                INSERT INTO order_items (
                    order_id, 
                    item_id, 
                    item_name, 
                    quantity,
                    price,
                    category
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                order_id,
                item['item_id'],
                item['item_name'],
                item['quantity'],
                float(item['price']),
                item['category1']
            ))
        
        # Clear the cart
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (session['username'],))
        
        # Clear payment details from session
        session.pop('payment_details', None)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Redirect to order confirmation page
        return redirect(url_for('order_confirmation', order_id=order_id))
        
    except mysql.connector.Error as err:
        print(f"Database error in complete_payment: {err}")
        if conn:
            conn.rollback()
            cursor.close()
            conn.close()
        flash('An error occurred while processing your payment. Please try again.')
        return redirect(url_for('cart'))

@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    if 'username' not in session:
        return redirect(url_for('login'))
        
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get order details
        cursor.execute("""
            SELECT * FROM orders WHERE order_id = %s AND user_id = %s
        """, (order_id, session['username']))
        order = cursor.fetchone()
        
        if not order:
            flash('Order not found', 'error')
            return redirect(url_for('home'))
            
        # Get order items
        cursor.execute("""
            SELECT * FROM order_items WHERE order_id = %s
        """, (order_id,))
        items = cursor.fetchall()
            
        cursor.close()
        conn.close()
        
        return render_template(
            'order_confirmation.html',
            order=order,
            items=items
        )
        
    except Exception as e:
        print(f"Error fetching order confirmation: {e}")
        flash('Error displaying order confirmation', 'error')
        return redirect(url_for('home'))

@app.route('/chef/login', methods=['GET', 'POST'])
def chef_login():
    if request.method == 'POST':
        chef_id = request.form.get('chef_id')
        password = request.form.get('password')
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM chefs WHERE chef_id = %s AND password = %s", (chef_id, password))
        chef = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if chef:
            session['chef_id'] = chef_id
            return redirect(url_for('chef_dashboard'))
        else:
            flash('Invalid credentials', 'error')
            
    return render_template('chef_login.html')

@app.route('/chef/dashboard')
def chef_dashboard():
    if 'chef_id' not in session:
        return redirect(url_for('chef_login'))
        
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get orders that need chef's attention (pending, cooking, or ready)
        cursor.execute("""
            SELECT o.*, 
                   GROUP_CONCAT(
                       CONCAT(oi.quantity, ' x ', oi.item_name)
                       SEPARATOR ', '
                   ) as order_items
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.status IN ('pending', 'cooking', 'ready')
            GROUP BY o.order_id
            ORDER BY 
                CASE o.status
                    WHEN 'pending' THEN 1
                    WHEN 'cooking' THEN 2
                    WHEN 'ready' THEN 3
                END,
                o.order_date DESC
        """)
        orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('chef_dashboard.html', orders=orders)
        
    except mysql.connector.Error as err:
        print(f"Database error in chef_dashboard: {err}")
        flash('Error loading orders', 'error')
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return render_template('chef_dashboard.html', orders=[])

@app.route('/chef/update_order', methods=['POST'])
def update_order():
    if 'chef_id' not in session:
        return redirect(url_for('chef_login'))
        
    order_id = request.form.get('order_id')
    new_status = request.form.get('status')
    
    # Validate status transition
    valid_transitions = {
        'pending': ['cooking'],
        'cooking': ['ready'],
        'ready': ['completed']
    }
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get current status
        cursor.execute("SELECT status FROM orders WHERE order_id = %s", (order_id,))
        current = cursor.fetchone()
        
        if not current:
            flash('Order not found', 'error')
            return redirect(url_for('chef_dashboard'))
            
        current_status = current['status']
        
        # Check if transition is valid
        if current_status in valid_transitions and new_status in valid_transitions[current_status]:
            # Update order status
            cursor.execute("""
                UPDATE orders 
                SET status = %s
                WHERE order_id = %s
            """, (new_status, order_id))
                
            conn.commit()
            flash(f'Order #{order_id} status updated to {new_status}', 'success')
        else:
            flash('Invalid status transition', 'error')
            
    except mysql.connector.Error as err:
        print(f"Error updating order: {err}")
        flash('Error updating order status', 'error')
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return redirect(url_for('chef_dashboard'))

@app.route('/chef/logout')
def chef_logout():
    session.pop('chef_id', None)
    return redirect(url_for('chef_login'))

if __name__ == '__main__':
    app.run(debug=True)