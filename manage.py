import csv
from app import app, db
from models import Customer, Product, ProductOrder, Order
# from sqlalchemy.sql.expression import random
from sqlalchemy import func , select
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
            next(reader)  # Skip the header row
            for row in reader:
                customers = Customer(name=row[0], phone=row[1], balance=random.randint(100,1000))
                db.session.add(customers)

        with open('data/products.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
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
            # Make an order
            order = Order(customer=customer)
            db.session.add(order)
            # Find a random product
            prod_stmt = db.select(Product).order_by(func.random()).limit(1)
            product = db.session.execute(prod_stmt).scalar()
            rand_qty = random.randint(10, 20)
            # Add that product to the order
            association_1 = ProductOrder(order=order, product=product, quantity=rand_qty)
            db.session.add(association_1)
            # Do it again
            prod_stmt = db.select(Product).order_by(func.random()).limit(1)
            product = db.session.execute(prod_stmt).scalar()
            rand_qty = random.randint(10, 20)
            association_2 = ProductOrder(order=order, product=product, quantity=rand_qty)
            db.session.add(association_2)
            # Commit to the database
            db.session.commit()
        
        

if __name__ == "__main__":
    drop_all()
    create_all()
    import_data()
    random_data()
    
    