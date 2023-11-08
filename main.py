# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line

from models import *
from peewee import DoesNotExist, fn
from setupdb import TRANSACTION_YEAR, TRANSACTION_WEEK, TRANSACTION_START_OF_DAY_HOUR, TRANSACTION_END_OF_DAY_HOUR
from utils.utils import random_date, random_time

def main():

    # search("Minty Fresh") # search for products by name and description
    search("foo_bar") # result: message: "Search term 'foo_bar' not found."

    # list_user_products(user_id=1) # For readability, I added the user_id as an argument.
    # list_user_products(user_id=3) # result is a list of products for user_id=3.
    # list_user_products(user_id=222222) # result: message: "User_id does not exist in table User."

    # list_products_per_tag(tag_id=1)
    # list_products_per_tag(tag_id=2)

    # add_product_to_catalog(1, "chanel_nr_1", "A timeless, elegant and sophisticated floral aldehyde synthetic fragrance", 10, 3)
    # add_product_to_catalog(3, "Parfum VI by Gianni Vive Sulman", "A financially painful olfactorial delight", 999.99, 2)
    # add_product_to_catalog(111111111, "bike", "Urban Traffic Legend", 499.92, 5) # result: message: "User_id does not exist in table User." 

    # update_stock(product_id=5, name=None, description=None, minimum_sales_price=None, quantity=10) # update quantity of existing product
    # update_stock(product_id=6, name="Shumukh", description="Welcome  to the world of olfactorial luxury and extravagance.", minimum_sales_price=1000, quantity=10) 

    # purchase_product(user_payment_method_id=1, product_id=3, price=10, quantity=1)
    # purchase_product(user_payment_method_id=2, product_id=4, price=10, quantity=55)

    # remove_product(product_id=5)

def search(term):
    '''
    requirements:
    1.	Search for products based on a term. Searching for 'sweater' should 
        yield all products that have the word 'sweater' in the name. This search 
        should be case-insensitive
    2. search for products by name and description
    '''
    query = Product.select().where(
    (Product.name.contains(term)) | (Product.description.contains(term))
    )
    if query.exists():
        for row in query:
            print(row.id, row.user_id, row.name, row.description)
            print('-' * 40)
        return query # best practice: return value for e.g. testing purposes (out of scope of this exercise)
    else:
        print(f"Search term '{term}' not found.")
        return f"Search term '{term}' not found."


    # if query == []:
    #     print(f"Search term '{term}' not found.")
    #     return f"Search term '{term}' not found."
    # for row in query:
    #     print(row.id, row.user_id, row.name, row.description)
    #     print('-' * 40)
    # return query # best practice: return value for e.g. testing purposes (out of scope of this exercise)


def search_with_spelling_mistakes(term):
    '''
    requirements:
    1. Finally the search should account for spelling mistakes made by users 
        and return products even if a spelling error is present.
    '''
    query = Product.select().where(
    (Product.name.contains(term)) | (Product.description.contains(term))
    )


    query1 = Product.select().where(fn.SOUNDEX(Product.name) == fn.SOUNDEX(term))

    # Use the fn.LEVENSHTEIN() function to calculate the edit distance between two strings
    # query2 = Product.select().where(fn.LEVENSHTEIN(Product.name, term) <= 2)

    if query == []:
        print(f"Search term '{term}' not found.")
        return f"Search term '{term}' not found."
    for row in query:
        print(row.id, row.user_id, row.name, row.description)
        print('-' * 40)
    return query # best practice: return value for e.g. testing purposes (out of scope of this exercise)



def list_user_products(user_id):
    try:
        user = User.get(User.id == user_id)
    except DoesNotExist:
        print("User_id does not exist in table User.")
        return "User_id does not exist in table User."
    print(user)
    print(type(user))
    user_products = user.products

    for product in user_products:
        print(product.id, product.name, product.description, product.minimum_sales_price, product.quantity)
        print('-' * 40) 
    return user_products

def list_products_per_tag(tag_id):
    query = (Product
             .select()
             .join(ProductTag)
             .join(Tag)
             .where(Tag.id == tag_id))
    products = [product.name for product in query]
    
    for product in products:
        print(product)
        print('-' * 40)
    return products

def add_product_to_catalog(user_id, product_name, description, minimum_sales_price, quantity):
    'requirements mention descripton, price and quantity as well, so I have added them to the function.'
    try:
        user = User.get(User.id == user_id)
    except DoesNotExist:
        print("User_id does not exist in table User.")
        return "User_id does not exist in table User."
    product = Product.create(user=user, name=product_name, description=description, minimum_sales_price=minimum_sales_price, quantity=quantity)
    return product 

def update_stock(product_id, name=None, description=None, minimum_sales_price=None, quantity=None):
    '''
        Requirements: update quantity of existing product.
        In addition to this, fn can also update name, description and minimum_sales_price.
    '''
    try:
        product = Product.get(Product.id == product_id)
    except DoesNotExist:
        print("Product_id does not exist in table Product.")
        return "Product_id does not exist in table Product."
    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if minimum_sales_price is not None:
        product.minimum_sales_price = minimum_sales_price
    if quantity is not None:
        product.quantity = quantity
    product.save()
    return product


from peewee import DoesNotExist

def purchase_product(user_payment_method_id, product_id, price, quantity):
    '''
    Requirements: user must have billing information.
    In my erd user has 1 or more payment methods. A user_payment_method_id uniquely identifies a buyer.
    So I use user_payment_method_id instead of buyer_id.
    Requirements: product must have a price. So I have added price as a fn argument.
    '''
    try:
        user_payment_method = UserPaymentMethod.get(UserPaymentMethod.id == user_payment_method_id)
    except DoesNotExist:
        print("User_payment_method_id does not exist in table UserPaymentMethod.")
        return "User_payment_method_id does not exist in table UserPaymentMethod."
    try:
        product = Product.get(Product.id == product_id)
    except DoesNotExist:
        print("Product_id does not exist in table Product.")
        return "Product_id does not exist in table Product."

    transaction = Transaction.create(product=product, 
                                     user_payment_method=user_payment_method, 
                                     quantity=quantity, 
                                     price=price, 
                                     date=random_date(TRANSACTION_YEAR, TRANSACTION_WEEK), 
                                     time=random_time(TRANSACTION_START_OF_DAY_HOUR, TRANSACTION_END_OF_DAY_HOUR))
    return transaction



def remove_product(product_id):
    try:
        product = Product.get(Product.id == product_id)
    except DoesNotExist:
        print("Product_id does not exist in table Product.")
        return "Product_id does not exist in table Product."
    product.delete_instance()
    return product

if __name__ == "__main__":
    main()