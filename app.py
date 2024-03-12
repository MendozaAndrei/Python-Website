from flask import *
import csv
from pathlib import Path
from db import db
from sqlalchemy import select
from models import Customer, Product, Order
app = Flask(__name__)





app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.instance_path = Path(".").resolve()
db.init_app(app)







#================================ pages ==========================

@app.route("/") 
def home():
    """This is the homepage. Nothing will be shown here"""
    return render_template("base.html")

@app.route("/customers")
def customers():
    """This is the customers page. It will show all the customers in the database."""
    statement = select(Customer).order_by(Customer.name)
    records = db.session.execute(statement)
    app_data = records.scalars()
    print(statement)
    return render_template("customers.html", customers=app_data)

@app.route("/products")
def products():
    statement = select(Product).order_by(Product.name)
    records = db.session.execute(statement)
    app_data = records.scalars()
    return render_template("products.html", products=app_data)


# This one does not work -- lacking data
@app.route("/orders")
def orders():
    statement=select(Order).order_by(Order.id)
    records = db.session.execute(statement)
    app_data = records.scalars()
    print("chicken")
    for order in app_data:
        print(order.items)
    return render_template("order.html", orders=app_data)


# Customer detail /customer/CUSTOMER_ID With links to all orders associated with the customer.
@app.route("/customers/<int:customer_id>")
def order_detail(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    list_of_orders = []
    for item in customer.orders[0].items:
        json_records = {
            "name": customer.name,
            "phone": customer.phone,
            "balance": customer.balance,
            
            "Order_name": item.product.name,
            "price": item.product.price
        }
        list_of_orders.append(json_records)
            
    # Adding more data into the list of orders.
    
            
    
    return render_template("customer_detail.html", customer=list_of_orders)
    
    
    pass        # Accessing the Customer json file and c`reating them into a json record. 
# =================================================================================================
'''
Each function is a route that returns a template to the url. The URL functions needs to be the same when
connecting to different pages in the HTML. This is very important.

The statements grabs the data from the database using an SQL command, and statement will hold that data.
records is what EXECUTES that command. Statement can be inside the execute() function. 

render_template is a functin that will load the HTML file and additional contents. The first position is REQUIRED to be
the HTML file. The second position is data that can be accessible to the HTML file. This allows us to load any information that wants to be loaded. 
'''
#================ API list of all the customers, products and orders ===============================
# This part creates the API list of the Website. 
@app.route("/api/customers")
def customers_json():
    
    statement = db.select(Customer).order_by(Customer.name)
    # Statement holds all the information about customer and what it is grabbing.
    results = db.session.execute(statement)
    
    customers = [] # output variable
    # appends the item into customers and which will be returned on the jsonify. 
    for customer in results.scalars():
        # Accessing the Customer json file and creating them into a json record. 
        json_record = {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "balance": customer.balance,
        }
        # JSON record is just the individual record there is in the csv file and that will be processed. 
        customers.append(json_record)
    return jsonify(customers)


# Crating an API set 
@app.route("/api/products")
def products_json():
    statement = db.select(Product).order_by(Product.name)
    results = db.session.execute(statement)
    products = [] # output variable
    for product in results.scalars():
        json_record = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
        }
        products.append(json_record)
        # Turns products into a json format. 
    return jsonify(products)
#creating  a route that takes in a URL parameter


# This does not work at all -- lacking data. 
@app.route("/api/orders")
def order_json():
    statement = db.select(Order).order_by(Order.id)
    results = db.session.execute(statement)
    data = [] # output variable
    for data_p in results.scalars():
        json_record = {
        "id": data_p.id,
        "customer_id": data_p.name,
        # "": data_p.price,
        # "quantity": data_p.quantity
        }
        data.append(json_record)
        # Turns products into a json format. 
    return jsonify(data)
#creating  a route that takes in a URL parameter
# =================================================================================================
'''
This allows the creation for API's. 

'''
#==================== Grabbing ID to get specific data in API ===============================
@app.route("/api/customers/<int:customers_id>")
def customer_detail_json(customers_id):
    statement = db.select(Customer).where(Customer.id == customers_id)
    result = db.session.execute(statement)
    products = []
    for product in result.scalars():
        json_record = {
            "id": product.id,
            "name": product.name,
            "phone": product.phone,
            "balance": product.balance
        }
        
        products.append(json_record)
        
    return jsonify(products)


@app.route("/api/products/<int:product_id>")
def product_detail_json(product_id):
    statement = db.select(Product).where(Product.id == product_id)
    result = db.session.execute(statement)
    products = []
    for product in result.scalars():
        json_record = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        }
        
        products.append(json_record)
        
    return jsonify(products)




#==========================================================================================================






#==================== METHODS ===============================
# All good
@app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def customer_delete(customer_id):
    customer = Customer.query.get(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return"deleted"


# All good
@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def product_delete(product_id):
    prod = Customer.query.get(product_id)
    db.session.delete(prod)
    db.session.commit()
    return"deleted"
    

# Giving the customer Balance 
@app.route("/api/customers/<int:customer_id>", methods=["PUT"])
def customer_update(customer_id):
    data = request.json
    customer = db.get_or_404(Customer, customer_id)

    if "balance" not in data:
        return "Invalid request", 400
    
    if not isinstance(data["balance"], (int, float)):
        return "Invalid request: balance", 400
    number = data["balance"]
    new_number = round(number,3)
    customer.balance = new_number
    print(customer.name)
    db.session.commit()
    customers()
    return "", 204



@app.route("/api/customers", methods=["POST"])
def customer_Post():
    data = request.json

    if "name" and "phone" not in data:
        return "Invalid Request", 400
    if not isinstance (data["name"], str):
        return "Invalid Request", 400
    if not isinstance(data["phone"], str):
        return "Invalid Request", 400
    
    
    db.session.add(Customer(name=data["name"], phone=data["phone"]))
    

    return "", 201



@app.route("/api/product", methods=["POST"])
def prodcut_post():
    data = request.json

    if "name" and "prince" not in data:
        return "Invalid Request", 400
    if not isinstance (data["name"], str):
        return "Invalid Request", 400
    if not isinstance(data["price"], str):
        return "Invalid Request", 400
    
    
    db.session.add(Product(name=data["name"], price=data["price"]))
    

    return "", 204

# This one will update the product
@app.route("/api/product/<int:product_id>", methods=['PUT'])
def product_put(product_id):
    data = request.json
    product = db.get_or_404(Product, product_id)

    print(data)
    attributes = ["name", "price", "quantity"]
    # Since data is a dicitonary, we can use the .get(value) to iterate thorugh the keys and set the value 
    updates = {attr: data.get(attr) for attr in attributes if attr in data}
    print(updates)
    if not updates:
        return "Invalid request", 400

    for attr, value in updates.items():
        setattr(product, attr, value)
    
    
    db.session.commit()
    

    return "", 204




    