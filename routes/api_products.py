from flask import Blueprint, jsonify, request
from db import db
from models import Product

api_products_bp = Blueprint("api_products", __name__)
@api_products_bp.route("/", methods=["GET"])
def prodcuct_json():
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
