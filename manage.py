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
                customers = Customer(name=row[0], phone=row[1], balance=random.randint(100,1000))
                db.session.add(customers)

        with open('data/products.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                products = Product(name=row[0], price=row[1], quantity=random.randint(0,100))
                db.session.add(products)

        db.session.commit()
        

# Grabbing random values
def random_data():
    with app.app_context():
        for x in range(100):
            cust_stmt = db.select(Customer).order_by(func.random()).limit(1)
            customer = db.session.execute(cust_stmt).scalar()

            order = Order(customer=customer, total=0)
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

            order.total = total
            db.session.commit()  
        

if __name__ == "__main__":
    drop_all()
    create_all()
    import_data()
    random_data()
    
    