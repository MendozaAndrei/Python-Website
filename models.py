from sqlalchemy import Boolean, Float, Numeric, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from db import db
from sqlalchemy.sql import func

#This'll create the table.
class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    name = mapped_column(String(200), nullable=False, unique=True) 
    phone = mapped_column(String(20), nullable=False) 
    balance = mapped_column(Numeric, nullable=False, default=100)
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
    price = mapped_column(Numeric, nullable=False) 
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
    total = db.Column(db.Float, nullable=False, default=0.0)
    strategy = mapped_column(String(20), nullable=False, default="adjust")
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
        
    def getTotal(self):
        res = 0
        for item in self.items:
            res += item.quantity*item.product.price
        return res
    
    
class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    order_id = mapped_column(Integer, ForeignKey(Order.id), nullable=False) 
    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    product = relationship("Product")
    order = relationship("Order")
    quantity = mapped_column(Integer, nullable=False, default=0)
    def to_json(self):
        return {
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }