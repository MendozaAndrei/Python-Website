from flask import Blueprint, jsonify, request
from db import db
from models import Customer, Product


api_customers_bp = Blueprint("api_customers", __name__)
@api_customers_bp.route("/", methods=["GET"])
def customers_json():
    statement = db.select(Customer).order_by(Customer.name)
    results = db.session.execute(statement)
    
    customers = [] #A list that will contain everything that needs to be known and will be pass through for iteration in the html file.
    for customer in results.scalars():
        json_record = {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "balance": customer.balance,
        } #This one however does not have the order things. Too lazy to do that. 
        customers.append(json_record)
    return jsonify(customers)





