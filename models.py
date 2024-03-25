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
    price = db.Column(db.String(20), nullable=False)
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
    # created = db.column(db.DateTime, server_default=db.func.now()) - part 3
    # processed = db.column(db.Boolean, default=None, nullable= True) - part 3, no need yet
    
    
    
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