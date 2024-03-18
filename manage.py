import csv
from app import app, db
from models import Customer, Product, ProductOrder, Order
# from sqlalchemy.sql.expression import random
from sqlalchemy import func


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
                customers = Customer(name=row[0], phone=row[1])
                db.session.add(customers)

        with open('data/products.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                products = Product(name=row[0], price=row[1])
                db.session.add(products)

        db.session.commit()
        

# Grabbing random values

        
        

if __name__ == "__main__":
    drop_all()
    create_all()
    import_data()
    with app.app_context():
        order1 = Order(customer_id = 1)
        order2 = Order(customer_id = 2)
        order3 = Order(customer_id = 5)
        po1 = ProductOrder(order_id = 1, product_id = 2, quantity = 3)
        po2 = ProductOrder(order_id = 1, product_id = 12, quantity = 4)
        po3 = ProductOrder(order_id = 1, product_id = 14, quantity = 3)
        po4 = ProductOrder(order_id = 1, product_id = 7, quantity = 8)
        po5 = ProductOrder(order_id = 2, product_id = 5, quantity = 7)
        po6 = ProductOrder(order_id = 2, product_id = 3, quantity = 9)
        po7 = ProductOrder(order_id = 3, product_id = 6, quantity = 1)
        db.session.add(order1)
        db.session.add(order2)
        db.session.add(order3)
        db.session.add(po1)
        db.session.add(po2)
        db.session.add(po3)
        db.session.add(po4)
        db.session.add(po5)
        db.session.add(po6)
        db.session.add(po7)
        db.session.commit()
        customer = db.get_or_404(Customer, 2)# customer is class and 1 is id
        # print(customer.orders[0].items[0].product.name)
        # print(customer.orders[0].items[0].product.price)
        # print(customer.orders[0].items[0].quantity)
        # print(customer.orders[0].items[1].product.name)
        # print(customer.orders[0].items[1].product.price)
        # print(customer.orders[0].items[1].quantity)
        # print(customer.orders[0].items[2].product.name)
        # print(customer.orders[0].items[2].product.price)
        # print(customer.orders[0].items[2].quantity)
        # print(customer.orders[0].items[3].product.name)
        # print(customer.orders[0].items[3].product.price)
        # print(customer.orders[0].items[3].quantity)
        # print(customer.orders[1].items[0].product.name)
        # print(customer.orders[1].items[0].product.price)
        # print(customer.orders[1].items[0].quantity)
        # print(customer.orders[1].items[1].product.name)
        # print(customer.orders[1].items[1].product.price)
        # print(customer.orders[1].items[1].quantity)
        # print(customer.orders[0].items[1].product.name)
        # print(len(customer.orders[0].items))
        list_of_orders = []
        for item in customer.orders[0].items:
            json_records = {
                "name": customer.name,
                "Order_name": item.product.name,
                "price": item.product.price
            }
            list_of_orders.append(json_records)

        for x in list_of_orders:
            print(x["name"])
            print(x["Order_name"])
            print(x["price"])
    app.run(debug=True, port=8888)
    