# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line

from models import *

from peewee import DoesNotExist
from peewee import fn
from Levenshtein import distance as lev

from playhouse.sqlite_ext import SqliteExtDatabase
from setupdb import TRANSACTION_YEAR, TRANSACTION_WEEK, TRANSACTION_START_OF_DAY_HOUR, TRANSACTION_END_OF_DAY_HOUR
from utils.utils import random_date, random_time

def main():

    # search("minty Fresh") # search for products by name and description
    # search("foo_bar") # result: message: "Search term 'foo_bar' not found."

    search_with_spelling_mistakes("Ruby") # search for products by name and description

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
    query = Product.select().where(fn.lower(Product.name).contains(term.lower()) | fn.lower(Product.description).contains(term.lower()))
    # (Product.name.contains(term)) | (Product.description.contains(term))
    # )
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


def levenshtein_distance(s1, s2):
    # source of this fn:  https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def search_with_spelling_mistakes(term): # activate 'term' as fn-argument 
    '''
    status: proof of concept works (231108)
    '''
    
    '''
    requirements:
    1. Finally the search should account for spelling mistakes made by users 
        and return products even if a spelling error is present.
    '''


    # Fetch data from the database
    query = Product.select()
    data = [(row, row.name) for row in query] 
    '''
    I create tuple instead of just row.name, because I
    need entire product-row instead of just the row.name in the final result.
    '''
    # Use the levenshtein_distance function to process the data
    results = [(item, (levenshtein_distance(item[1], 'KrimsoM Sky') < 4)) for item in data] 
    # 2do: hard-coded search term: 'KrimsoM Sky' --> 2do: make fn argument.
    # legenda: item[1] == row.name == product.name
    # 2do: make '4' a fn-argument, so levenshtein's distance becomes dynamic. 

    for result in results:
        print(result)
        # 2do next: filter the rows with result 'True' in each row (look at last value in the tuple for each row)
    

    '''
    e.g. of result:

    ((<Product: 1>, 'Crimson Sky'), True)
    ((<Product: 2>, 'Minty Fresh'), False)
    ((<Product: 3>, 'Golden Harvest'), False)
    ((<Product: 4>, 'Sapphire Sea'), False)
    ((<Product: 5>, 'Copper Canyon'), False)
    ((<Product: 6>, 'Emerald Isle'), False)
    ((<Product: 7>, 'Midnight Sun'), False)
    ((<Product: 8>, 'Silver Lining'), False)
    ((<Product: 9>, 'Ruby Red'), False)
    ((<Product: 10>, 'Ocean Breeze'), False)
    
    '''

    # query = Product.select().where(
    # (Product.name.contains(term)) | (Product.description.contains(term))
    # )

#    query = "SELECT * FROM product WHERE name = 'Crimson Sky'" # works (1 result)
#     query = "SELECT * FROM product WHERE name = 'Crimson Sk'" # works ( 0 results)
#     query = "SELECT * FROM product WHERE LEVENSHTEIN(name, 'Crimson Sky') <= 2;" # works ( 0 results)
#     cursor = db.execute_sql(query)
#     for row in cursor.fetchall():
#         print(row) 
    # query = Product.select().where((lev(Product.name, term) < 1))
    # query2 = Product.select().where(fn.editdist(Product.description, term) <= 2)
    # query = query1 | query2

    # # Execute the query to get the results
    # results = query.execute()
    # print('results:')
    # print(results)
    # print('bla')
    # # Print the results
    # for product in results:
    #     print(product , product.name, product.description)

    # # Use the fn.LEVENSHTEIN() function to calculate the edit distance between two strings
    # query = Product.select().where(fn.LEVENSHTEIN(Product.name, term) <= 2)

    # query = Product.select().where(fn.SOUNDEX(Product.description) == fn.SOUNDEX(term))

    # # Use the fn.LEVENSHTEIN() function to calculate the edit distance between two strings
    # query4 = Product.select().where(fn.LEVENSHTEIN(Product.description, term) <= 2)

    # query = query1 | query2 | query3 | query4

    # if query.exists():
    #     for row in query:
    #         print(row.id, row.user_id, row.name, row.description)
    #         print('-' * 40)
    #     return query # best practice: return value for e.g. testing purposes (out of scope of this exercise)
    # else:
    #     print(f"Search term '{term}' not found.")
    #     return f"Search term '{term}' not found."



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