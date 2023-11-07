# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line

from models import *

def main():

    # search("Crimson")
    list_user_products(1)


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
    # print(query)
    for row in query:
        print(row.id, row.user_id, row.name, row.description)
        print('-' * 40)


def list_user_products(user_id):
    user = User.get(User.id == user_id)
    user_products = user.products

    for product in user_products:
        print(product.id, product.name, product.description, product.minimum_sales_price, product.quantity)
        print('-' * 40) 



def list_products_per_tag(tag_id):
    pass


def add_product_to_catalog(user_id, product):
    pass


def update_stock(product_id, new_quantity):
    pass


def purchase_product(product_id, buyer_id, quantity):
    pass

def remove_product(product_id):
    pass


if __name__ == "__main__":
    main()