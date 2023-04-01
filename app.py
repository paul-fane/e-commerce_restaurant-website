from cs50 import SQL
from flask import Flask, jsonify, flash, redirect, render_template, request, session 
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import uuid

from helpers import apology, login_required, admin_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///takeaway.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template ("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username") or not request.form.get("password"):
            flash("Input missed!")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM customer WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hashPassword"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["customerID"]
        session["name"] = rows[0]["customerName"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure input was submitted
        if not request.form.get("username") or not request.form.get("fullname") or not request.form.get("email") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Input missed", 400)

        # Ensure password match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("Passwords don`t much", 400)

        # Ensure username is available
        rows = db.execute("SELECT * FROM customer WHERE username = ?", request.form.get("username"))

        # If is one row =>(username = not available) else if 0 row =>(username = available)
        if len(rows) == 1:
            return apology("Username is not available", 400)
        # created at
        created_at = datetime.now()
        
        # Insert user in database (ID=>autoincrement  //  cash=>10000 default)
        db.execute("INSERT INTO customer (customerName, username, email, hashPassword, created_at) VALUES(?, ?, ?, ?, ?)", request.form.get("fullname"), request.form.get("username"), request.form.get("email"),  generate_password_hash(request.form.get("password")), created_at)

        # Select the user
        row = db.execute("SELECT * FROM customer WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = row[0]["customerID"]
        session["name"] = row[0]["customerName"]

        # Redirect user to home page
        flash('Successfully register')
        return redirect("/")

    # GET
    return render_template("register.html")


# PICKUP MENU
@app.route("/pickup-menu")
def pickup():
    # Select all the distinct category that have at least 1 product not archived
    categorys = db.execute("SELECT DISTINCT category FROM product WHERE archive = ?",0)
    # Select all the products
    products = db.execute("SELECT * FROM product")
    return render_template ("menu-take-away.html", categorys=categorys, products=products)


@app.route("/search-products")
def searchProduct():
    # Select the products
    products = db.execute("SELECT * FROM product")
    return jsonify(products)


# Account
@app.route("/account")
@login_required
def info():
    """Account info"""

    # Select the current user
    info = db.execute("SELECT * FROM customer WHERE customerID = ?", session.get("user_id"))

    # Select orders of current user
    orders = db.execute("SELECT * FROM orders  WHERE customerID = ? ORDER BY orderID DESC", session.get("user_id"))
    return render_template ("account.html", customer=info, orders=orders)


@app.route('/account/orders/<int:id_order>')
@login_required
def orderDetails(id_order):
    """Order Details, accoun"""

    order = db.execute("SELECT * FROM orders WHERE orderID = ?", id_order)[0]

    # Handle inexistent productID
    if not order:
        flash("Something went wrong, order not foud")
        return redirect("/account")

    order_details = db.execute("SELECT * FROM order_details WHERE uniqueID = ?", order['uniqueID'])
    
    # For every productID in the order fetch the details from product database
    products = []
    for item in order_details:
        product = db.execute("SELECT * FROM product WHERE productID = ?", item['productID'])[0]
        itemDetail = {
            "productName": product['productName'],
            "category": product['category'],
            "quantity": item['quantity'] 
        }
        products.append(itemDetail)

    return render_template("orderDetails.html", order=order, products=products)
        

@app.route("/cart", methods=["GET", "POST"])
def cart():
    """Cart"""
    
    # POST
    if request.method == "POST":

        # For every item in cart, add the price based of the quantity to the totalPrice variable
        totalPrice = 0

        # Create a unique ID for every order
        uniqueUUID = uuid.uuid4()

        # Time now and current user
        created_at = datetime.now()
        current_user = session.get("user_id")
        
        # Data from javascript
        data = request.json
        cart = data.get("cart", "")
        date = data.get("date", "")
        type = data.get("type", "")
        address = data.get("address", "")

        # Ensure input was submitted
        if not cart:
            return jsonify("Products missed!")

        if not date:
            return jsonify("Date missed!")
            
        if not type:
            return jsonify("Type missed! Choose betwen Delivery and Pickup")

        if type == "Delivery" and not address:
            return jsonify("Address missed!")

        if type == "Pickup":
            address = ''

        # Add every item in the order details table
        for item in cart:
            print(item['id'])
            db.execute("INSERT INTO order_details (uniqueID, productID, quantity) VALUES(?, ?, ?)", uniqueUUID.hex, item['id'], int(item['quantity']))
            
            # Calculate the total price to insert in the orders table
            price = db.execute("SELECT price FROM product WHERE productID = ?", item['id'])[0]
            totalPrice += (price['price'] * float(item['quantity']))
        
        # Add the order to the database
        db.execute("INSERT INTO orders (uniqueID, customerID, created_at, pickup_delivery_time, total_price, type, address) VALUES(?, ?, ?, ?, ?, ?, ?)", uniqueUUID.hex, current_user, created_at,  date, totalPrice , type, address)

        flash("Successfuly order!")
        return jsonify("Successfuly order!")

    # GET
    return render_template ("cart.html")


# ADMIN
@app.route("/admin")
@login_required
def admin():
    """Administrator"""

    # The admin is the id number 1, only him has access to the admin area
    id = session["user_id"]
    if id == 1:
        return render_template ("admin.html")
    else:
        flash("Sorry, you must be the Admin to access the admin page!")
        return redirect("/")

@app.route("/admin/customers")
@login_required
@admin_required
def customers():
    """Administrator/customers"""

    # Select all the users
    customers = db.execute("SELECT * FROM customer ORDER BY customerID DESC")
    return render_template("customers.html", customers=customers)

@app.route("/admin/customers/add", methods=["GET", "POST"])
@login_required
@admin_required
def addCustomers():
    """Register user, admin area"""

    # POST
    if request.method == "POST":

        # Ensure input was submitted
        if not request.form.get("username") or not request.form.get("fullname") or not request.form.get("email") or not request.form.get("password") or not request.form.get("confirmation"):
            flash("Input missed")
            return redirect("/admin/customers/add")

        # Ensure password match
        elif request.form.get("confirmation") != request.form.get("password"):
            flash("Passwords don`t much")
            return redirect("/admin/customers/add")

        # Ensure username is available
        rows = db.execute("SELECT * FROM customer WHERE username = ?", request.form.get("username"))

        # If is one row =>(username = not available) else if 0 row =>(username = available)
        if len(rows) == 1:
            flash("Username is not available")
            return redirect("/admin/customers/add")

        created_at = datetime.now()

        # Insert user in database 
        db.execute("INSERT INTO customer (customerName, username, email, hashPassword, created_at) VALUES(?, ?, ?, ?, ?)", request.form.get("fullname"), request.form.get("username"), request.form.get("email"),  generate_password_hash(request.form.get("password")), created_at)

        # Redirect user to home page
        flash('Successfully register')
        return redirect("/admin/customers/add")

    # GET
    return render_template("addCustomer.html")


@app.route('/admin/customers/<int:id_customer>/change', methods=["GET", "POST"])
@login_required
@admin_required
def changeCustomers(id_customer):
    """Change user, admin area"""
    
    # POST
    if request.method == "POST":

        # Ensure input was submitted
        if not request.form.get("username") or not request.form.get("fullname") or not request.form.get("email") or not request.form.get("password") or not request.form.get("confirmation"):
            flash("Input missed")
            return redirect(f"/admin/customers/{id_customer}/change")

        # Ensure password match
        elif request.form.get("confirmation") != request.form.get("password"):
            flash("Passwords don`t much")
            return redirect(f"/admin/customers/{id_customer}/change")

        # Search the user
        rows = db.execute("SELECT * FROM customer WHERE customerID = ?", id_customer)
        if len(rows) != 1:
            flash("Something went wrong, user to change not foud")
            return redirect("/admin/customers")


        # Insert user in database 
        db.execute("UPDATE customer SET customerName = ?, username = ?, email = ?, hashPassword = ? WHERE customerID = ?", request.form.get("fullname"), request.form.get("username"), request.form.get("email"),  generate_password_hash(request.form.get("password")), id_customer)

        # Redirect user to home page
        flash('Successfully changed')
        return redirect("/admin/customers")

    # GET
    costumer_detail = db.execute("SELECT * FROM customer WHERE customerID = ?", id_customer)

    # Handle error of inexistance customerID
    if not costumer_detail:
        flash("Something went wrong, customer to change not foud")
        return redirect("/admin/customers")

    return render_template("changeCustomer.html", costumer_detail=costumer_detail[0])


@app.route("/admin/products")
@login_required
@admin_required
def products():
    """Products"""

    # The list of products
    products = db.execute("SELECT * FROM product ORDER BY productID DESC")

    # The list of archived products
    archivedList = db.execute("SELECT * FROM product WHERE archive = 1")

    # Create a flag to show if the archived list is empty
    if len(archivedList) == 0:
        noArchive = True
    else:
        noArchive = False
    return render_template("products.html", products=products, noArchive=noArchive)
    

@app.route("/admin/products/add", methods=["GET", "POST"])
@login_required
@admin_required
def addProducts():
    """Add products"""

    # POST
    if request.method == "POST":

        # Ensure input was submitted
        if not request.form.get("productName") or not request.form.get("price") or not request.form.get("category"):
            flash("Input missed")
            return redirect("/admin/products/add")

        # Check Image
        image = request.form.get("image")
        if image == None:
            image = ''

        # If the archive checkbox input was checked will returne 1 (true)
        archive = request.form.get("change-archive")

        # Else will return None and will remain 0 (false)
        if archive == None:
            archive = 0

        # Ensure product name is available
        rows = db.execute("SELECT * FROM product WHERE productName = ?", request.form.get("productName"))

        # If is one row =>(productName = not available) else if 0 row =>(productName = available)
        if len(rows) == 1:
            flash("product Name is not available")
            return redirect("/admin/products/add")

        # Insert product in database
        db.execute("INSERT INTO product (productName, price, archive, category, image) VALUES(?, ?, ?, ?, ?)", request.form.get("productName"), request.form.get("price"), archive, request.form.get("category"), image)

        # Redirect user to home page
        flash('Successfully product added')
        return redirect("/admin/products/add")

    # GET
    categorys = db.execute("SELECT DISTINCT category FROM product")
    return render_template("addProduct.html", categorys=categorys)

@app.route('/admin/products/<int:id_product>/change', methods=["GET", "POST"])
@login_required
@admin_required
def changeProducts(id_product):
    """Change product, admin area"""

    # POST 
    if request.method == "POST":

        # Ensure input was submitted
        if not request.form.get("productName") or not request.form.get("price") or not request.form.get("category"):
            flash("Input missed")
            return redirect(f"/admin/products/{id_product}/change")

        # Check Image
        image = request.form.get("image")
        if image == None:
            image = ''
        
        # If the archive checkbox input was checked will returne 1 (true)
        archive = request.form.get("change-archive")

        # Else will return None and will remain 0 (false)
        if archive == None:
            archive = 0

        # Check if the Id is in the database and the product exists
        rows = db.execute("SELECT * FROM product WHERE productID = ?", id_product)
        if len(rows) != 1:
            flash("Something went wrong, product to change not foud")
            return redirect("/admin/products")

        # Edit user in database 
        db.execute("UPDATE product SET productName = ?, price = ?, archive = ?, category = ?, image = ? WHERE productID = ?", request.form.get("productName"), request.form.get("price"), archive, request.form.get("category"), image, id_product)

        # Redirect user 
        flash('Successfully changed')
        return redirect("/admin/products")
    
    # GET
    product_detail = db.execute("SELECT * FROM product WHERE productID = ?", id_product)

    # Handle inexistent productID
    if not product_detail:
        flash("Something went wrong, product to change not foud")
        return redirect("/admin/products")

    # List of all the existent categorys
    categorys = db.execute("SELECT DISTINCT category FROM product")
    return render_template("changeProduct.html", product_detail=product_detail[0], categorys=categorys)



@app.route("/admin/orders")
@login_required
@admin_required
def orders():
    """Orders"""

    # Select orders and users
    orders = db.execute("SELECT * FROM orders ORDER BY orderID DESC")
    customers = db.execute("SELECT customerID, customerName FROM customer")

    return render_template("orders.html", orders=orders, customers=customers)


@app.route('/admin/orders/<int:id_order>/change', methods=["GET", "POST"])
@login_required
@admin_required
def changeOrder(id_order):
    """Change order, admin area"""
    
    if request.method == "POST":

        # Ensure input was submitted
        if not request.form.get("uniqueID") or not request.form.get("customerID") or not request.form.get("created_at") or not request.form.get("pickup_delivery_time") or not request.form.get("total_price") or not request.form.get("type"):
            flash("Input missed")
            return redirect(f"/admin/orders/{id_order}/change")

        # Search the order
        rows = db.execute("SELECT * FROM orders WHERE orderID = ?", id_order)
        if len(rows) != 1:
            flash("Something went wrong, order to change not foud")
            return redirect("/admin/orders")

        if request.form.get("type") == 'Delivery' and not request.form.get("address"):
            flash("Address input missed! For Delivery, address required!")
            return redirect(f"/admin/orders/{id_order}/change")

        if request.form.get("address"):
            address = request.form.get("address")
        else:
            address = ""

        # Insert order in database 
        db.execute("UPDATE orders SET uniqueID = ?, customerID = ?, created_at = ?, pickup_delivery_time = ?, total_price = ?, type = ?, address = ? WHERE orderID = ?", request.form.get("uniqueID"), request.form.get("customerID"), request.form.get("created_at"),  request.form.get("pickup_delivery_time"), request.form.get("total_price"), request.form.get("type"), address, id_order)

        # Redirect user to home page
        flash('Successfully changed')
        return redirect("/admin/orders")

    # GET

    # Select the order and all the products in the order
    order = db.execute("SELECT * FROM orders WHERE orderID = ?", id_order)[0]
    # Handle error of inexistance customerID
    if not order:
        flash("Something went wrong, order to change not foud")
        return redirect("/admin/orders")
    order_details = db.execute("SELECT * FROM order_details WHERE uniqueID = ?", order['uniqueID'])

    # For every productID in the order fetch the details from product database
    products = []
    for item in order_details:
        product = db.execute("SELECT * FROM product WHERE productID = ?", item['productID'])[0]
        itemDetail = {
            "productName": product['productName'],
            "quantity": item['quantity'] 
        }
        products.append(itemDetail)

    return render_template("changeOrder.html", order=order, products=products)


@app.route('/search-orders', methods=["GET", "POST"])
@login_required
@admin_required
def searchOrders():

    # POST
    if request.method == "POST":
        # Data from javascript
        data = request.json
        type = data.get("type", "")
        customerName = data.get("customerName", "")
        uniqueID = data.get("uniqueID", "")
        pickup_deliveryTime = data.get("pickup_deliveryTime", "")

        # If type input empty
        if not type:
            type = ''

        # If uniqueID input empty
        if not uniqueID:
            uniqueID = ''

        # If pickup_deliveryTime input empty
        if not pickup_deliveryTime:
            pickup_deliveryTime = ''

        # If customerName
        if customerName:
            # Search for name like the input customerName
            customers = db.execute("SELECT * FROM customer WHERE customerName LIKE ?", "%" + customerName + "%")

            # If the length of the search == 0 then => no user with that name
            if len(customers) == 0:
                return jsonify('No user with that name!')

            # Else for any customer with the name like customerName => advanced search (like type, like uniqueID, like pickup_deliveryTime)
            orders = []
            for person in customers:
                # Search orders for each customer
                results = db.execute("SELECT * FROM orders WHERE type LIKE ? AND customerID = ? AND uniqueID LIKE ? AND pickup_delivery_time LIKE ?", "%" + type + "%" , person['customerID'] , "%" + uniqueID + "%" , "%" + pickup_deliveryTime + "%")
                
                for result in results:
                    # For every order of each customer => add each order in the orders list
                    orders.append(result)

            customer = db.execute("SELECT * FROM customer")
            return jsonify(orders, customer)

        # Else if customerName input empty
        orders = db.execute("SELECT * FROM orders WHERE type LIKE ? AND uniqueID LIKE ? AND pickup_delivery_time LIKE ?", "%" + type + "%" , "%" + uniqueID + "%" , "%" + pickup_deliveryTime + "%")
        customer = db.execute("SELECT * FROM customer")
        return jsonify(orders, customer)
