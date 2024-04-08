from flask import Blueprint, jsonify, request, redirect, url_for
from db import db
from models import Order, ProductOrder, Customer, Product

api_orders_bp = Blueprint("api_orders", __name__)

# All orders data
@api_orders_bp.route("/", methods=["GET"])
def orders_json():
    statement = db.select(Order).order_by(Order.id) 
    results = db.session.execute(statement)
    orders = []
    for order in results.scalars().all(): 
        orders.append(order.to_json())
    return jsonify(orders)

# Create new order
@api_orders_bp.route("/", methods = ["POST"])
def create_order():
    data = request.json
    if "customer_id" not in data or "items" not in data:
        return "Missing customer_id or items", 400
    for each in data["items"]:
        if "name" not in each or "quantity" not in each:
            return "Missing name or quantity", 400
    customer = db.get_or_404(Customer, data["customer_id"])
    items = data["items"]
    new_order = Order(customer = customer)
    db.session.add(new_order)

    for item in items:
        stm = db.select(Product).where(Product.name == item["name"])
        product = db.session.execute(stm).scalar()
        if product is None:
            return f"Invalid product!", 400
        # if product.availability < item["quantity"]:
        #     return f"Invalid quantity for product {item["name"]}, only {product.availability} left!", 400
        po = ProductOrder(order = new_order, product = product, quantity = item["quantity"])
        db.session.add(po)

    db.session.commit()
    return "", 204

api_order_id_bp = Blueprint("api_order_id", __name__)
@api_order_id_bp.route("/", methods=["PUT"])
def process_order_put(order_id):
    print(":LSKDJF:LSDKJF:SDLKJFSDLK:JFS:DLKJFDS")
    order = Order.query.get(order_id)
    data = request.get_json()

    if order is None:
        return jsonify({"error": "Order not found"}), 404

    if not data.get('process', False):
        return jsonify({"error": "Invalid request"}), 400

    strategy = data.get('strategy', 'adjust')
    print(strategy)
    print(data["strategy"])
    if strategy not in ['adjust', 'reject', 'ignore']:
        return jsonify({"error": "Invalid strategy"}), 400

    [success, message] = order.process_method(data["strategy"])
    if not success:
        return jsonify({"error": message}), 400
    else:
        success = jsonify({"message": message})
    return jsonify({"message": "milk"}), 200


# Proess an order (no json required, default strategy = "adjust")
@api_order_id_bp.route("/", methods=["POST"])
def process_order_no_json(order_id):
    order = db.get_or_404(Order, order_id)
    order.process_method()
    return redirect(url_for("orders"))




# Proess an order (json required)
# @api_order_id_bp.route("/", methods=["PUT"])
# def process_order(order_id):
#     data = request.json

#     strategy = None
#     if ("process" not in data) or (data["process"] is not True):
#         return "Invalid input, cant process!", 400
    
#     if ("strategy" in data) and (data["strategy"] not in ["reject", "ignore", "adjust"]):
#         return "Invalid input, cant process!", 400

#     if "strategy" not in data:
#         strategy = "adjust"
#     else:
#         strategy = data["strategy"]
    
#     order = db.get_or_404(Order, order_id)
#     order.process(strategy)
#     return redirect(url_for("orders"))
# @api_orders_bp.route("<int:order_id>", methods=["PUT"])



# @api_orders_bp.route("/", methods=["POST"])
# def order_update():
#     # Parse the incoming JSON data
#     data = request.get_json()

#     # Validate the data
#     if 'customer_id' not in data or 'items' not in data:
#         return jsonify({"message": "Invalid data."}), 400

#     # Create a new Order object
#     new_order = Order(customer_id=data['customer_id'])

#     # Add the new order to the database
#     db.session.add(new_order)

#     # For each item in items
#     for item in data['items']:
#         # Find the corresponding Product
#         product = Product.query.filter_by(name=item['name']).first()

#         # If the product does not exist, rollback and return an error message
#         if product is not None:
#             product_order = ProductOrder(order=new_order, product=product, quantity=item['quantity'])


#         # Create a new ProductOrder object

#         # Add the new ProductOrder to the database
#         db.session.add(product_order)

#     # Commit the transaction
#     try:
#         db.session.commit()
#     except ValueError:
#         db.session.rollback()
#         return jsonify({"message": "An error occurred while creating the order."}), 500

#     # Return a response
#     return jsonify(new_order.to_json()), 201

# Note, if we use normal route, in template order_list.html, 
# we need to change the form action to 
# action="{{ url_for('process_order_no_json', order_id=order.id) }}"