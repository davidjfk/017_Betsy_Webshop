from models import *
import os, sys
import random

sys.path.append('c:\\dev\\pytWinc\\betsy-webshop')
sys.path.append('c:\\dev\\pytWinc\\betsy-webshop\\utils')
from utils.utils import assign_payment_methods, assign_tags, create_sample_data_product
from utils.utils import create_sample_data_user, random_date, random_time


# CONFIGURATION:
TRANSACTION_YEAR = 2028
TRANSACTION_WEEK = 26
TRANSACTION_START_OF_DAY_HOUR = 8
TRANSACTION_END_OF_DAY_HOUR = 21
PRODUCT_RANGE = 6 # choose 4 or higher (because list transactions below assumes product_range >= 4)
# product_assortment == the collection of different products in the Betsy Webshop
NR_OF_PRODUCTS_FOR_EACH_PRODUCT = 30 
NR_OF_TAGS_PER_PRODUCT_LOWER_BOUNDARY = 2
NR_OF_TAGS_PER_PRODUCT_UPPER_BOUNDARY = 6
NR_OF_PAYMENT_METHODS_PER_USER_LOWER_BOUNDARY = 1
NR_OF_PAYMENT_METHODS_PER_USER_UPPER_BOUNDARY = 4
'''
if product range = apple, laptop, banana, then nr_of_products_for_each_product = 30 means that there are 30 apples, 30 laptops, 30 bananas in the Betsy Webshop after running setupdb.py
'''

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

    
    # if there are e.g. 4 payment methods, then I needs this: "payment_method_ids = [1,2,3,4]", 5 payment methods: "payment_method_ids = [1,2,3,4,5]", etc.
    payment_method_ids = [(payment_methods.index(sublist) + 1) for sublist in payment_methods] # possible to add paymentmethod later on, wthout breaking the code.
    # goal: for each user, assign a random number of payment methods:
    user_list = []
    for i in range(len([user for user in users if isinstance(user, dict)])):
        user_list.append({'user_id': i + 1}) # 
        user_list[i]['payment_methods'] = random.sample(payment_method_ids, random.randint(NR_OF_PAYMENT_METHODS_PER_USER_LOWER_BOUNDARY, NR_OF_PAYMENT_METHODS_PER_USER_UPPER_BOUNDARY))
    # print(user_list)
    user_paymentmethods = []
    for user in user_list:
        for payment_method in user['payment_methods']:
            user_paymentmethods.append([user['user_id'], payment_method])
    # print(user_paymentmethods)
    # problem: following list works, but is hard-coded:
    # user_paymentmethods = [
    #     [1, 2],
    #     [1, 3],
    #     [2, 2],
    #     [2, 4],
    #     [3, 1],
    #     [3, 2],
    #     [3, 3],
    #     [3, 4],
    #     [4, 1],
    #     [4, 2],
    #     [5, 3],
    #     [5, 4],
    #     [6, 1],
    #     [6, 2],
    #     [6, 4],
    # ]
    for user_paymentmethod in user_paymentmethods:
        UserPaymentMethod.create(user=user_paymentmethod[0], payment_method=user_paymentmethod[1])


    products = create_sample_data_product(PRODUCT_RANGE, NR_OF_PRODUCTS_FOR_EACH_PRODUCT)
    for product in products:
        Product.create(user_id=product["user_id"], name=product["name"], description=product["description"], minimum_sales_price=product["minimum_sales_price"], quantity=product["quantity"])


    '''
    Hard-coded list of transactions (on purpose, so you can quickly manually create or tweak custom transaction(s) for testing purposes):
    '''
    transactions = [
        [1, 2, 3, 3],
        [2, 3, 4, 4],
        [2, 2, 5, 5],
        [2, 4, 6, 6],
        [3, 1, 2, 3], # selling break-even
        [3, 2, 3, 7],
        [3, 3, 4, 7],
        [3, 4, 5, 9],
        [4, 1, 3, 6],
        [4, 2, 4, 11],
        [5, 3, 6, 8],
        [5, 4, 7, 7],
        [6, 1, 7, 3], # selling at a loss
        [6, 2, 5, 10],
        [6, 4, 10, 27], # selling at a huge profit
    ]
    '''
    product_id and price have the same number: e.g.
    product_id=2, price=2 euro
    product_id=3, price=3 euro
    product_id=4, price=4 euro
    etc.

    This is done on purpose to make it easier to read the data.

    e.g. last nested list in list transactions above:
    product_id = 4, so the minimum_viable_price is 4 euro. Seller sells product for 27, 
    making a huge profit.
    '''
    for transaction in transactions:
        Transaction.create(user_payment_method=transaction[0], product=transaction[1], quantity=transaction[2], price=transaction[3], date=random_date(TRANSACTION_YEAR, TRANSACTION_WEEK), time=random_time(TRANSACTION_START_OF_DAY_HOUR, TRANSACTION_END_OF_DAY_HOUR))


    tags = ["book", "clothing", "electronics", "fashion", "finance", "food", "games", "home_appliance", "household_goods" "insurance", "literature", "mobile_phone", "music", "musical_instrument", "pet", "science", "sport", "shoes", "software", "sport", "toys", "travel"]
    for tag in tags:
        Tag.create(name=tag)


    product_list = []
    for product in products:
        product_list.append({'name': product})
    products_with_tags = assign_tags(products, tags, NR_OF_TAGS_PER_PRODUCT_LOWER_BOUNDARY, NR_OF_TAGS_PER_PRODUCT_UPPER_BOUNDARY)  
    # print(products_with_tags)
    for product_with_tags in products_with_tags:
        for tag in product_with_tags['tags']:
            ProductTag.create(product=product_with_tags['name'], tag=tag)


    db.close()

if __name__ == "__main__":
    main()

