from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from db import db

# creates the table for us.
class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    phone = mapped_column(String(20), nullable=False)
    balance = mapped_column(Numeric(10,2), nullable=False, default=0)
    
    # Creates a relationship to Product
    orders = relationship("Order", back_populates="customer")
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "balance": self.balance,
        }
        
class Product(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    price = mapped_column(String(20), nullable=False)
    quantity = mapped_column(Integer, nullable=False, default=0)
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
        }
    

class Order(db.Model):
    '''
    This one connects to customer only
    id
    total
    customer_id - foreign key
    
    '''
    # id = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    # total = mapped_column(Integer, nullable=False)
    # customer_id = mapped_column("Customers", back_pupulates="orders")
    # items = mapped_column("Customer")
    # product_order = relationship("ProductOrder")
    
    
    id = mapped_column(Integer, primary_key=True)
    customer_id = mapped_column(Integer, ForeignKey('customer.id'), nullable=False)
    
    
    # Creates a relationship with Order and
    customer = relationship("Customer", back_populates="orders")
    items = relationship("ProductOrder", back_populates="order")
    
    
    
    def to_json(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "customer": self.customer,
            "item": self.items,
        }



class ProductOrder(db.Model):
    '''
    This is connected to Order 
    This is connected to Product
    id
    order_id
    product_id
    quanitity
    
    '''
    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = mapped_column(Integer, default=0, nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "order_id": self.order_id,
            "quantity": self.quantity,
            "order":self.order,
            "product": self.product
        }
        
# class Order(db.Model):
#     id = mapped_column(Integer, primary_key=True, autoincrement=True)
#     total = mapped_column(Numeric)
#     customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False, unique=True)
#     customer = relationship("Customer", back_populates="orders")
    
# class ProductOrder(db.Model):
#     id = mapped_column(Integer, primary_key=True, nullable=False,autoincrement=True)
#     quanitty = mapped_column(Integer, nullable=False)
#     order_id = mapped_column(Integer, ForeignKey(Order.id), nullable=False)
#     product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
#     pass
    
    
    
