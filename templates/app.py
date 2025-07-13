from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# DB Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="drink_inventory"
)
cursor = db.cursor(dictionary=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search = request.form['search']
        cursor.execute("SELECT * FROM drinks WHERE name LIKE %s", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM drinks")
    drinks = cursor.fetchall()
    return render_template('index.html', drinks=drinks)

@app.route('/add', methods=['GET', 'POST'])
def add_drink():
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        quantity = request.form['quantity']
        price = request.form['price']
        cursor.execute("INSERT INTO drinks (name, brand, quantity, price) VALUES (%s, %s, %s, %s)", 
                       (name, brand, quantity, price))
        db.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_drink(id):
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        quantity = request.form['quantity']
        price = request.form['price']
        cursor.execute("UPDATE drinks SET name=%s, brand=%s, quantity=%s, price=%s WHERE id=%s", 
                       (name, brand, quantity, price, id))
        db.commit()
        return redirect('/')
    cursor.execute("SELECT * FROM drinks WHERE id=%s", (id,))
    drink = cursor.fetchone()
    return render_template('edit.html', drink=drink)


@app.route('/delete/<int:id>')
def delete_drink(id):
    cursor.execute("DELETE FROM drinks WHERE id=%s", (id,))
    db.commit()
    return redirect('/')