import csv
from app import app, db
from models import Customer, Product, ProductOrder, Order
# from sqlalchemy.sql.expression import random
from sqlalchemy import func , select
from sqlalchemy import and_
import random

def drop_all():
    with app.app_context():
        db.drop_all()

def create_all():
    with app.app_context():
        db.create_all()

def import_data():
    with app.app_context():
        with open('data/customers.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                customers = Customer(name=row[0], phone=row[1], balance=random.choice([100, 200, 300, -1000]))
                db.session.add(customers)

        with open('data/products.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                products = Product(name=row[0], price=row[1], quantity=10)
                db.session.add(products)

        db.session.commit()
        

def random_data():
    with app.app_context():
        for x in range(4):
            cust_stmt = db.select(Customer).order_by(func.random()).limit(1)
            customer = db.session.execute(cust_stmt).scalar()

            order = Order(customer=customer)
            db.session.add(order)
            db.session.commit()

            total = 0  
            for _ in range(2):  
                prod_stmt = db.select(Product).order_by(func.random()).limit(1)
                product = db.session.execute(prod_stmt).scalar()

                quantity = random.randint(1, 5)
                total += float(product.price) * int(quantity)

                product_order = ProductOrder.query.filter_by(order_id=order.id, product_id=product.id).first()

                if product_order:
                    product_order.quantity += quantity
                else:
                    product_order = ProductOrder(order_id=order.id, product_id=product.id, quantity=quantity)
                    db.session.add(product_order)

            # order.total = total  # Remove this line
            db.session.commit()  




# def process_method():
#     with app.app_context():
#         # Needed - Product Quantity to be compared to Product Quantity
        
#         # productOrder = db.select(ProductOrder).where(ProductOrder.quantity > Product.quantity)
#         # product_quantity = db.select(Product.quantity)
#         # product_order_quantity = db.select(ProductOrder.quantity)
#         order = db.select(Order).where(Order.processed == None)
#         if order:
#             for product_order in order.product_orders:
#                 product = Product.query.get(product_order.product_id)
#                 if product.quantity < product_order.quantity:
#                     product_order.quantity = product.quantity
#                     product.quantity = 0
#                 else:
#                     product.quantity -= product_order.quantity
#             order.processed = True
#             db.session.commit()
    
#     """
#     This function processes the order
#     Not processing order that's already process
#     Current customer balance must be >0
#     if customer ordered more of a product than is available in store, 
#         adjust(default) - the order is adjusted to match the quantity available in the store. 
        
#     """
    
        

if __name__ == "__main__":
    drop_all()
    create_all()
    import_data()
    with app.app_context(): 
        
        order3 = Order(customer_id = 1)
        order4 = Order(customer_id = 5)
        order5 = Order(customer = db.session.execute(db.select(Customer).order_by(func.random()).limit(1)).scalar())
        po3 = ProductOrder(order_id = 2, product_id = 2, quantity = 10)
        po4 = ProductOrder(order_id = 2, product_id = 12, quantity = 10)
        po5 = ProductOrder(order_id = 2, product_id = 14, quantity = 10)
        po6 = ProductOrder(order_id = 2, product_id = 7, quantity = 10)
        po7 = ProductOrder(order_id = 3, product_id = 5, quantity = 7)
        po8 = ProductOrder(order_id = 3, product_id = 3, quantity = 9)
        po9 = ProductOrder(order_id = 4, product_id = 2, quantity = 1)
        po10 = ProductOrder(order_id = 5, product_id = 6, quantity = 4)
        po11 = ProductOrder(order_id = 5, product_id = 11, quantity = 2)
        po12 = ProductOrder(order_id = 5, product_id = 7, quantity = 2)
        db.session.add(order3)
        db.session.add(order4)
        db.session.add(order5)
        db.session.add(po3)
        db.session.add(po4)
        db.session.add(po5)
        db.session.add(po6)
        db.session.add(po7)
        db.session.add(po8)
        db.session.add(po9)
        db.session.add(po10)
        db.session.add(po11)
        db.session.add(po12)
        db.session.commit()
    random_data()
    
    