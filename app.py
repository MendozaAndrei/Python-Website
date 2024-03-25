from flask import *
import csv
from pathlib import Path
from db import db
from sqlalchemy import select
from flask import redirect, url_for
from models import Customer, Product, Order, ProductOrder
app = Flask(__name__)





app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.instance_path = Path(".").resolve()
db.init_app(app)







#================================ pages ==========================
"""This holds all pages with relevant information inside them"""
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
    '''This is the products page. It will show all the products in the database.'''
    statement = select(Product).order_by(Product.name)
    records = db.session.execute(statement)
    app_data = records.scalars()
    return render_template("products.html", products=app_data)


@app.route("/orders")
def orders():
    '''THis is the orders page. It will show all the orders listed in the database.'''
    statement = select(Order).order_by(Order.id)
    records = db.session.execute(statement)
    app_data = records.scalars()
    return render_template("orders.html", orders=app_data)

# ======================== Specific Detail Pages ===============================    
"""
"""
# Will show a webpage with the details of the order with the specific order_id
@app.route("/orders/<int:order_id>")
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)

    customer = Customer.query.get(order.customer_id)

    order.total = sum(float(item.product.price) * float(item.quantity) for item in order.items)

    return render_template("order_details.html", order=order, customer=customer)

# Customer detail /customer/CUSTOMER_ID With links to all orders associated with the customer.
@app.route("/customer/<int:customer_id>")
def customer_detail(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    orders = Order.query.filter_by(customer_id=customer_id).all()

    for order in orders:
        order.total = sum([float(item.product.price) * float(item.quantity) for item in order.items])
    return render_template("customer_detail.html", customer=customer, orders=orders)    # Accessing the Customer json file and creating them into a json record. 
# =================================================================================================




#================ API list of all the customers, products and orders ===============================
# This part creates the API list of the Website. 
@app.route("/api/customers")
def customers_json():
    
    statement = db.select(Customer).order_by(Customer.name)
    results = db.session.execute(statement)
    
    customers = [] # output variable
    for customer in results.scalars():
        json_record = {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "balance": customer.balance,
        }
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
    return jsonify(products)


@app.route("/api/orders")
def order_json():
    statement = db.select(Order).order_by(Order.id)
    results = db.session.execute(statement)
    data = []
    for data_p in results.scalars():
        json_record = {
            "id": data_p.id,
            "customer_id": data_p.customer_id,
            
        }
        data.append(json_record)
    return jsonify(data)

@app.route("/api/orders/<int:order_id>")
def order_detail_json(order_id):
    statement = db.select(Order).where(Order.id == order_id)
    result = db.session.execute(statement)
    data = []
    for data_p in result.scalars():
 
        items = [{"name": item.product.name, "quantity": item.quantity} for item in data_p.items]
        json_record = {
            "id": data_p.id,
            "customer_id": data_p.customer_id,
            "items": items,  
        }
        data.append(json_record)
    return jsonify(data)


#creating  a route that takes in a URL parameter


# =================================================================================================
'''


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
@app.route("/api/orders", methods=["POST"])
def create_order():
    # Extract JSON data from the request
    data = request.get_json()

    if "customer_id" not in data:
        return jsonify({"error": "Missing customer_id"}), 400
    if "items" not in data or not isinstance(data["items"], list) or not data["items"]:
        return jsonify({"error": "Invalid items"}), 400

    customer = Customer.query.get(data["customer_id"])
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    order = Order(customer_id=customer.id)
    db.session.add(order)

    for item_data in data["items"]:
        if "name" not in item_data or "quantity" not in item_data:
            return jsonify({"error": "Invalid item data"}), 400

        product = Product.query.filter_by(name=item_data["name"]).first()
        if product:
            product_order = ProductOrder(order_id=order.id, product_id=product.id, quantity=item_data["quantity"])
            db.session.add(product_order)

    db.session.commit()

    return jsonify(order.to_json()), 201

@app.route("/orders/<int:order_id>/delete", methods=["POST"])
def order_delete(order_id):
    order = db.get_or_404(Order, order_id)
    db.session.flush()
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("orders"))



# =================================================================================================
"""
PUT is basically UPDATING the data. The data being updated NEEDS to exist, or else it will return an error that the data cannot be found
POST is basically ADDING the data. The data being added NEEDS to be in the database, or else it will return an error that the data cannot be found
DELETE is basically DELETING the data. The data being deleted NEEDS to be in the database, or else it will return an error that the data cannot be found




"""

if __name__=="__main__":
    app.run(debug=True, port=8888)


    