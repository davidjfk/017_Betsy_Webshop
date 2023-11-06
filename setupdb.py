from models import *
import os, sys
sys.path.append('c:\\dev\\pytWinc\\betsy-webshop')
sys.path.append('c:\\dev\\pytWinc\\betsy-webshop\\utils')
from utils.utils import create_sample_data_product, create_sample_data_user

def main():
    # delete_database()
    populate_database()

def delete_database():
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "database.db")
    if os.path.exists(database_path):
        os.remove(database_path)

def populate_database():

    db.connect()

    db.create_tables([User, Product, PaymentMethod, Transaction, Tag, ProductTag, UserPaymentMethod])

    users = create_sample_data_user(6)
    for user in users:
        print(user)
        User.create(last_name=user["last_name"], first_name=user["first_name"], phone_number=user["phone_number"], email=user["email"], street=user["street"], house_number=user["house_number"], postal_code=user["postal_code"], city=user["city"], country=user["country"], password=user["password"])


    payment_methods = [
        ["credit_card", "Pay after the purchase transaction", "world", True, 0.035],
        ["direct_debit",  "bank-to-bank transfer system", "Europe", True, 0.00],     
        ["ideal", "bank-to-bank transfer system", "Netherlands", True, 0.11],
        ["paypal", "worldwide payment system for individuals and businesses", "world", True, 0.025]
    ]
    for payment_method in payment_methods:
        PaymentMethod.create(name=payment_method[0], description=payment_method[1], active=payment_method[3], fee=payment_method[4])

    user_paymentmethods = [
        [1, 2],
        [1, 3],
        [2, 2],
        [2, 4],
        [3, 1],
        [3, 2],
        [3, 3],
        [3, 4],
        [4, 1],
        [4, 2],
        [5, 3],
        [5, 4],
        [6, 1],
        [6, 2],
        [6, 4],
    ]
    for user_paymentmethod in user_paymentmethods:
        UserPaymentMethod.create(user=user_paymentmethod[0], payment_method=user_paymentmethod[1])

    products = create_sample_data_product(6)
    for product in products:
        Product.create(user_id=product["user_id"], name=product["name"], description=product["description"], price=product["price"], quantity=product["quantity"])

    transactions = [
        [1, 2, 3, ],
        [1, 3, 4, ],
        [2, 2, 5, ],
        [2, 4, 6, ],
        [3, 1, 2, ],
        [3, 2, 3, ],
        [3, 3, 4, ],
        [3, 4, 5, ],
        [4, 1, 3, ],
        [4, 2, 4, ],
        [5, 3, 6, ],
        [5, 4, 7, ],
        [6, 1, 4, ],
        [6, 2, 5, ],
        [6, 4, 6, ],
    ]
    for transaction in transactions:
        Transaction.create(user_payment_method=transaction[0], product=transaction[1])


    db.close()

if __name__ == "__main__":
    main()