from flask import Blueprint, jsonify, request
from db import db
from models import Order

api_orders_bp = Blueprint("api_orders", __name__)
@api_orders_bp.route("/", methods=["GET"])
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