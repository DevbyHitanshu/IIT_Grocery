from flask import Flask, render_template, request, redirect, session , url_for
from logging import FileHandler, WARNING
import sqlite3
import hashlib
from database import Database

db = Database('fdatabase.db')
db.create_tables()

app = Flask(__name__, template_folder='template')
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

app.secret_key = 'your_secret_key'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        password = request.form['Password']
        user_type = request.form['UserType']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect('fdatabase.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (Name, Email, Password, User_type) VALUES (?, ?, ?, ?)",
                           (name, email, hashed_password, user_type))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', register_message='Email already exists. Please choose a different email.')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        conn = sqlite3.connect('fdatabase.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE Email = ?", (email,))

        user = cursor.fetchone()
        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == user[3]:
                # Update the active_session column to 1
                cursor.execute("UPDATE users SET active_session = ? WHERE id = ?", (1, user[0]))
                conn.commit()  # Commit the transaction
                conn.close()

                
                session['user_id'] = user[0]
                session['logged_in'] = True
                session['user_type'] = user[4]
                session['user_name'] = user[1] 
                if user[4] == 'admin':
                    return redirect('/homeadmin')
                else:
                    return redirect('/')
            else:
                conn.close()
                return render_template('login.html', register_message='Invalid email or password')
        else:
            conn.close()
            return render_template('login.html', register_message='Invalid email or password')
    else:
        return render_template('login.html')
    
@app.route('/logout', methods=['GET'])
def logout():
    if 'user_id' in session:
        user_id = session['user_id']
        session.clear()  # Clear all session variables

        # Update active_session to 0 in the database
        conn = sqlite3.connect('fdatabase.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET active_session = ? WHERE id = ?", (0, user_id))
        conn.commit()
        conn.close()

    return redirect('/')


@app.route('/homeadmin', methods=['GET', 'POST'])
def store_manager_home():
    conn = sqlite3.connect('fdatabase.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'create_section' in request.form:
            section_name = request.form['section_name']
            cursor.execute("INSERT INTO sections (sec) VALUES (?)", (section_name,))
            conn.commit()
            conn.close()
            return redirect(url_for('store_manager_home'))  


        elif 'edit_section_btn' in request.form:
            edit_section_id = request.form['edit_section']
            sections = cursor.execute("SELECT * FROM sections").fetchall()
            return render_template('homeadmin.html', sections=sections, edit_section=edit_section_id)
        
        elif 'update_section_btn' in request.form:
            new_section_name = request.form['new_section_name']
            edit_section_id = request.form['edit_section']
            cursor.execute("UPDATE sections SET sec = ? WHERE id = ?", (new_section_name, edit_section_id))
            conn.commit()
            sections = cursor.execute("SELECT * FROM sections").fetchall()
            conn.close()
            return redirect(url_for('store_manager_home'))

        elif 'remove_section_btn' in request.form:
            remove_section_id = request.form['remove_section']
            print(remove_section_id)
            confirm_remove = request.form.get('confirm_remove')
            if confirm_remove:
                cursor.execute("DELETE FROM sections WHERE id=?", (remove_section_id,))
                conn.commit()
                sections = cursor.execute("SELECT * FROM sections").fetchall()
                conn.close()
                return redirect(url_for('store_manager_home'))


    cursor.execute("SELECT * FROM sections")
    sections = cursor.fetchall()
    conn.close()
    return render_template('homeadmin.html', sections=sections)

@app.route('/product', methods=['GET', 'POST'])
def store_manager_product():
    conn = sqlite3.connect('fdatabase.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'create_product' in request.form:
            product_name = request.form['product_name']
            product_price = request.form['product_price']
            product_category = request.form['product_category']
            cursor.execute("INSERT INTO products (name, price, section_id) VALUES (?, ?, ?)", (product_name, product_price, product_category))
            conn.commit()
            products = cursor.execute("SELECT * FROM products").fetchall()
            sections = cursor.execute("SELECT * FROM sections").fetchall()
            conn.commit()
            conn.close()
            return redirect(url_for('store_manager_product'))

        elif 'edit_product_btn' in request.form:
            edit_product_id = request.form['edit_product']
            products = cursor.execute("SELECT * FROM products").fetchall()
            return render_template('product.html', products=products, edit_product=edit_product_id)
        
        elif 'update_product_btn' in request.form:
            new_product_name = request.form['new_product_name']
            new_product_price = request.form['new_product_price']
            edit_product_id = request.form['edit_product']  # Corrected field name
            cursor.execute("UPDATE products SET name = ?, price = ? WHERE id = ?", (new_product_name, new_product_price, edit_product_id))  # Assuming id is the correct identifier for a product
            conn.commit()
            products = cursor.execute("SELECT * FROM products").fetchall()
            conn.close()
            return redirect(url_for('store_manager_product'))


        elif 'remove_product_btn' in request.form:
            remove_product_id = request.form['remove_product']
            confirm_remove = request.form.get('confirm_remove')
            if confirm_remove:
                cursor.execute("DELETE FROM products WHERE id=?", (remove_product_id,))
                conn.commit()
                products = cursor.execute("SELECT * FROM products").fetchall()
                conn.close()
                return redirect(url_for('store_manager_product'))

    # Fetch products and render template for GET requests
    products = cursor.execute("SELECT * FROM products").fetchall()
    sections = cursor.execute("SELECT * FROM sections").fetchall()

    conn.close()
    return render_template('product.html', products=products, sections=sections)

@app.route('/', methods=['GET'])
def user_products():
    conn = sqlite3.connect('fdatabase.db')
    cursor = conn.cursor()

    section_id = request.args.get('section')
    search_query = request.args.get('search')

    query = "SELECT products.id, products.name, products.price FROM products INNER JOIN sections ON products.section_id = sections.id"
    params = []

    if section_id:
        query += " WHERE sections.id = ?"
        params.append(section_id)

    if search_query:
        if section_id:
            query += " AND products.name LIKE ?"
        else:
            query += " WHERE products.name LIKE ?"
        params.append(f"%{search_query}%")

    cursor.execute(query, tuple(params))
    products = cursor.fetchall()

    sections = cursor.execute("SELECT * FROM sections").fetchall()
    conn.close()

    return render_template('user_products.html', products=products, sections=sections, user_name=session.get('user_name'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    product_name = request.form.get('product_name')
    product_price = request.form.get('product_price')
    quantity = int(request.form.get('quantity'))
    print(product_id)

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({'product_id': product_id, 'name': product_name, 'price': product_price, 'quantity': quantity})
    
    # Add the cart item to the database
    conn = sqlite3.connect('fdatabase.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (product_name, product_price, quantity) VALUES (?, ?, ?)",
                   (product_name, product_price, quantity))
    conn.commit()
    conn.close()
    
    return redirect(url_for('user_products'))




@app.route('/cart')
def cart():
    conn = sqlite3.connect('fdatabase.db')
    cursor = conn.cursor()
    cart_items = cursor.execute("SELECT * FROM cart").fetchall()
    conn.close()

    total_price = sum(float(item[2]) * item[3] for item in cart_items if item[2] and item[3])

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    #if 'cart' in session:
    #    session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]

    conn = sqlite3.connect('fdatabase.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
