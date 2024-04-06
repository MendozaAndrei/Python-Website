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
    '''
    backref is a way to add a new property to the "other" class in many to many relationships. 

    back_populates is used in conjunction with a corresponding relationship field in the "other" class.
    It requires to define a relationship on both sides and is necessary for many-to-many relationship. 
    
    in short, backref is faster and less hasle to use compared to back_populates. 
    
    
    
    '''
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
                # if the quantity of the product is less than the quantity of the product order
                if product.quantity < product_order.quantity:
                    product_order.quantity = product.quantity
                    # The customer will get the only available quantity, and the quantity of the product is set to 0
                    product.quantity = 0
                    
                else:
                # If the quantity of the product is more than the quantity of the product order
                # It will decrease the number of the quantity. 
                    product.quantity -= product_order.quantity
            self.processed = True
            
            
        
        elif strategy == "reject":
            """
            This part is a little iffy.
            It is to reject the entire order if the quanitty of any product is LESS than the quanity of the product order.
            If the quanitty of the product is LESS than the quanity of the product order, the order will be rejected, and won't be processed at all.
            """
            for product_order in self.product_orders:
                product = Product.query.get(product_order.product_id)
                if product.quantity < product_order.quantity:
                    self.processed = False
                    return
            for product_order in self.product_orders:
                product = Product.query.get(product_order.product_id)
                product.quantity -= product_order.quantity
            self.processed = True
            
        elif strategy == "ignore":
            # ignores
            self.processed = False
        else:
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