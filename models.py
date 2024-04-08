from sqlalchemy import Boolean, Float, Numeric, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from db import db
from sqlalchemy.sql import func
from datetime import datetime

#This'll create the table.
class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    name = mapped_column(String(200), nullable=False, unique=True) 
    phone = mapped_column(String(20), nullable=False) 
    balance = mapped_column(Numeric(10,2), nullable=False, default=100)
    orders = relationship("Order")
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "balance": self.balance,
            'order_ids': [order.id for order in self.orders]
        }

class Product(db.Model):
    '''
    backref is a way to add a new property to the "other" class in many to many relationships. 

    back_populates is used in conjunction with a corresponding relationship field in the "other" class.
    It requires to define a relationship on both sides and is necessary for many-to-many relationship. 
    
    in short, backref is faster and less hasle to use compared to back_populates. 
    
    
    
    '''
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(200), nullable=False, unique=True)
    # price = db.Column(db.Float, nullable=False)
    # quantity = db.Column(db.Integer, nullable=False, default=0)
    # product_orders = db.relationship('ProductOrder', backref='product_ref')
    
    id = mapped_column(Integer, primary_key=True) 
    name = mapped_column(String(200), nullable=False, unique=True) 
    price = mapped_column(Numeric(10,2), nullable=False) 
    quantity = mapped_column(Integer, nullable=False, default=10)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
        }

class Order(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False) 
    created = mapped_column(DateTime, default=func.now())
    processed = mapped_column(DateTime, nullable=True, default=None)
    customer = relationship("Customer", back_populates="orders")
    items = relationship("ProductOrder", back_populates="order")
    strategy = mapped_column(String(20), nullable=False, default="adjust")
    # Worse part of this project so far ommai
    def process_method(self, strategy):
        self.processed = datetime.now()
        self.strategy = strategy  # Set the strategy attribute

        if strategy == "adjust":
            for product_order in self.items:
                # Check if quantity is negative
                if product_order.quantity < 0:
                    return (False, "Order cannot be processed due to negative quantity")

                product = Product.query.get(product_order.product_id)
                if product.quantity < product_order.quantity:
                    product_order.quantity = product.quantity
                    product.quantity = 0
                else:
                    product.quantity -= product_order.quantity
            db.session.commit()
            return (True, "Order processed successfully")
        elif strategy == "reject":
            for product_order in self.items:
                product = Product.query.get(product_order.product_id)
                if product.quantity < product_order.quantity:
                    self.processed = None
                    db.session.commit()
                    return (False, "")
            db.session.commit()
            return (True, "")
        elif strategy == "ignore":
            db.session.commit()
            return (True, "")
            
    def getTotal(self):
        return sum(item.product.price * item.quantity for item in self.order_items)
    
    
    def to_json(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'created': self.created,
            'processed': self.processed,
            'strategy': self.strategy,
            'total': self.getTotal()
            # 'items': [item.to_json() for item in self.items]
        }
    
    
class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    order_id = mapped_column(Integer, ForeignKey(Order.id), nullable=False) 
    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    product = relationship("Product")
    order = relationship("Order")
    quantity = mapped_column(Integer, nullable=False, default=0)
    quantity = mapped_column(Integer, nullable=False, default=0)
    def to_json(self):
        return {
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }