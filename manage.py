# Import necessary modules and classes from Flask
from flask.cli import FlaskGroup
from app import create_app, db
from flask import current_app

# Import datetime, csv, and os modules
from datetime import datetime
import csv
import os

# Import models from the app
from app.models.users import Users
from app.models.products import Products
from app.models.editor.customer import Customer
from app.models.editor.supplier import Supplier
from app.models.editor.company_products import CompanyProducts
from app.models.editor.company_orders import CompanyOrders
from app.models.editor.order_item import OrderItems

# Create Flask CLI group using the create_app function from the app module
cli = FlaskGroup(create_app=create_app)

# Define user data in JSON format
user_json = [...]

# Define product data in JSON format
product_json = [...]

# Function to recreate the database
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

# Function to seed the database with user and product data
def seeder():
    # Seed Users
    for user in user_json:
        Users.create(user.get("name"), user.get("email"), user.get("password"), user.get("contact"))

    # Seed Products
    for product in product_json:
        Products.create(product.get("name"), product.get("image"), product.get("rating"),
                        product.get("marked_price"), product.get("selling_price"))

    # Seed the editor data from CSV files
    # Customer
    with open("app/editor_data/customer.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                Customer.create(int(row[0]), row[1], row[2], row[3], row[4], row[5])
            except:
                pass

    # Supplier
    with open("app/editor_data/supplier.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                Supplier.create(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6])
            except:
                pass

    # CompanyProducts
    with open("app/editor_data/company_products.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                CompanyProducts.create(int(row[0]), row[1], int(row[2]), float(row[3]), row[4], int(row[5]))
            except:
                pass

    # CompanyOrders
    with open("app/editor_data/company_orders.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                CompanyOrders.create(int(row[0]), datetime.strptime(row[1], "%b %d %Y %I:%M:%S:%f%p"),
                                     int(row[2]), float(row[3]), int(row[4]))
            except:
                pass

    # OrderItems
    with open("app/editor_data/order_items.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                OrderItems.create(int(row[0]), int(row[1]), int(row[1]), float(row[1]), int(row[1]))
            except:
                pass

# Command to recreate and seed the database
@cli.command()
def rsd():
    # Check if the application environment is allowed for database seeding
    # if current_app.config.get('ENV') not in ('development', 'test', 'testing'):
    #     print("ERROR: seed-db only allowed in development and testing env.")
    #     return
    
    # Recreate the database and seed it with data
    recreate_db()
    seeder()

# Run the CLI if the script is executed directly
if __name__ == '__main__':
    cli()