from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from db import db

#This'll create the table.
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Integer, nullable=False, default=0)
    orders = db.relationship('Order', backref='customer')

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "balance": self.balance,
            'order_ids': [order.id for order in self.orders]
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    product_orders = db.relationship('ProductOrder', backref='product_ref')

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    product_orders = db.relationship('ProductOrder', backref='order_ref', cascade='all, delete-orphan')
    created = db.Column(db.DateTime, default=db.func.now())
    processed = db.Column(db.Boolean, default=None, nullable= True)
    strategy = db.Column(db.String(20), default="adjust")
    # Worse part of this project so far ommai
    def process_method(self, strategy="adjust"):
        if strategy == "adjust":
            for product_order in self.product_orders:
                product = Product.query.get(product_order.product_id)
                if product.quantity < product_order.quantity:
                    product_order.quantity = product.quantity
                    product.quantity = 0
                else:
                    product.quantity -= product_order.quantity
            self.processed = True
        elif strategy == "reject":
            for product_order in self.product_orders:
                product = Product.query.get(product_order.product_id)
                if product.quantity < product_order.quantity:
                    # Reject the order
                    self.processed = False
                    return
            # If we haven't returned yet, all products are available in sufficient quantity
            for product_order in self.product_orders:
                product = Product.query.get(product_order.product_id)
                product.quantity -= product_order.quantity
            self.processed = True
        elif strategy == "ignore":
            # Ignore the order
            self.processed = False
        else:
            # Default strategy
            pass
    
    
class ProductOrder(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    def to_json(self):
        return {
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }