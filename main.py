# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
from models import *
from peewee import DoesNotExist, fn
from setupdb import TRANSACTION_YEAR, TRANSACTION_WEEK, TRANSACTION_START_OF_DAY_HOUR, TRANSACTION_END_OF_DAY_HOUR
from utils.utils import levenshtein_distance, random_date, random_time, remove_duplicates
from rich.table import Table
from rich.console import Console

def main():

    # Important: before calling the following fns, first reset the configuration variables at the start of setupdb.py to their default values. 

    # search("minty Fresh") # 1 search result
    search("Mi") # 4 search results
    # search("foo_bar") # result: message: "Search term 'foo_bar' not found."

    # search_with_spelling_mistakes("KrimsoM Sky", levenshstein_comparison_variable = 2) # 0 search result
    # search_with_spelling_mistakes("KrimsoM Sky", levenshstein_comparison_variable = 4) # 1 search result
    # search_with_spelling_mistakes("Midnight Sun", levenshstein_comparison_variable = 10) # 2 search results
    # search_with_spelling_mistakes("Midnight Sun", levenshstein_comparison_variable = 12) # 6 search results
    # search_with_spelling_mistakes("q", levenshstein_comparison_variable = 4) # 0 search results
    '''
    Practically, the higher the levenshtein_comparison_variable number, the more spelling mistakes are allowed when 
    searching for a product name or description.

    Theoretically, the Levenshtein distance is a string metric for measuring the difference between two sequences. 
    Informally, the Levenshtein distance between two words is the minimum number of single-character 
    edits (insertions, deletions or substitutions) required to change one word into the other.
    source: https://en.wikipedia.org/wiki/Levenshtein_distance
    '''

    # list_user_products(user_id=1) 
    # list_user_products(user_id=3) 
    # list_user_products(user_id=222222) # result: message: "User_id does not exist in table User."

    # list_products_per_tag(tag_id=1)
    # list_products_per_tag(tag_id=2)
    # list_products_per_tag(tag_id=333333) # result: message: "Tag_id '333333' not found."

    # add_product_to_catalog(1, "chanel_nr_1", "A timeless, elegant and sophisticated floral aldehyde synthetic fragrance", 10, 3)
    # add_product_to_catalog(3, "Parfum VI by Gianni Vive Sulman", "A financially painful olfactorial delight", 1999.99, 2)
    # add_product_to_catalog(111111111, "bike", "Urban Traffic Legend", 499.92, 5) # result: message: "User_id does not exist in table User." 

    # update_stock(product_id=5, name=None, description=None, minimum_sales_price=None, quantity=11) # update quantity of existing product
    # update_stock(product_id=6, name="Shumukh", description="Welcome  to the world of olfactorial luxury and extravagance.", minimum_sales_price=1000, quantity=10) 

    # show_all_transactions()

    # purchase_product(user_payment_method_id=1, product_id=5, price=10, quantity=1) # test preparation: select existing ids.
    # purchase_product(user_payment_method_id=2, product_id=4, price=10, quantity=55) # test preparation: select existing ids.

    # remove_product(product_id=10) # select product_id that is NOT used in transaction(s). 
    # Expected result: can be removed. Notice that the product tags in junction table ProductTag are also removed.
    
    # remove_product(product_id=3) # select product_id that IS used in transaction(s). 
    # Expected result: cannot be removed

def search(search_term):
    '''
    requirements:
    1.	Search for products based on a term. Searching for 'sweater' should 
        yield all products that have the word 'sweater' in the name. This search 
        should be case-insensitive
    2. search for products by name and description
    '''
    query = Product.select().where(fn.lower(Product.name).contains(search_term.lower()) | fn.lower(Product.description).contains(search_term.lower()))
    if query.exists():
        table = Table(title=f"Search term: << {search_term} >>, searching without spelling mistakes", show_header=True, header_style="bold magenta")
        table.add_column("product_id", justify="right")
        table.add_column("user_id", justify="right")
        table.add_column("product_name", justify="left")
        table.add_column("description", justify="left")
        table.add_column("price", justify="right")
        table.add_column("quantity", justify="right")
        
        for row in query:
            table.add_row(str(row.id), str(row.user_id), row.name, row.description, str(int(row.minimum_sales_price)), str(row.quantity))
        console = Console()
        console.print(table)
        return query # best practice: return value for e.g. testing purposes later on (out of scope of this exercise)
    else:
        print(f"Search term '{search_term}' not found.")
        return f"Search term '{search_term}' not found."


def search_with_spelling_mistakes(search_term: str, levenshstein_comparison_variable: int, remove_duplicates = remove_duplicates): # activate 'term' as fn-argument    
    '''
    requirements:
    1. Finally the search should account for spelling mistakes made by users 
        and return products even if a spelling error is present.
    '''
    query = Product.select()
    product_rows = [[row.id, row.user.id, row.name, row.description, int(row.minimum_sales_price), row.quantity] for row in query] 
    results_of_search_on_product_name = [[product_row, (levenshtein_distance(product_row[2], search_term) < levenshstein_comparison_variable)] for product_row in product_rows] 
    results_of_search_on_product_description = [[product_row, (levenshtein_distance(product_row[3], search_term) < levenshstein_comparison_variable)] for product_row in product_rows]
    results_combined = results_of_search_on_product_name + results_of_search_on_product_description
    results_that_match_search_term = [row for row in results_combined if row[1] == True] # 'True' means: there is a match.
    results_that_match_search_term = [result[0] for result in results_that_match_search_term]
    '''
        Search term could match both name and description of a product. If so, the product is added twice to the list.
        To prevent this: remove duplicates.
    '''
    results_that_match_search_term = remove_duplicates(results_that_match_search_term)
    table = Table(title=f"Search term: << {search_term} >>, searching with possible spelling mistakes", show_header=True, header_style="bold magenta")
    table.add_column("product_id", justify="right")
    table.add_column("user_id", justify="right")
    table.add_column("product_name", justify="left")
    table.add_column("description", justify="left")
    table.add_column("price", justify="right")
    table.add_column("quantity", justify="right")

    for row in results_that_match_search_term:
        print(row)
        '''
        examples of row:
        [1, 1, 'Crimson Sky', 'A luxurious and elegant fragrance that will transport you to the clouds.', 1, 30]
        [2, 12, 'Minty Fresh', 'A refreshing and invigorating scent that will awaken your senses.', 2, 30]
        [3, 5, 'Golden Harvest', 'A warm and comforting aroma that will remind you of home.', 3, 30]
        '''
        table.add_row(str(row[0]), str(row[1]), row[2], row[3], str(int(row[4])), str(row[5]))
    console = Console()
    console.print(table)
    return results_that_match_search_term


def list_user_products(user_id):
    try:
        user = User.get(User.id == user_id)
    except DoesNotExist:
        print("User_id does not exist in table User.")
        return "User_id does not exist in table User."
    print(user)
    print(type(user))
    user_products = user.products

    table = Table(title=f"List Products for user_id: << {user_id} >>", show_header=True, header_style="bold magenta")
    table.add_column("product_id", justify="right")
    table.add_column("user_id", justify="right")
    table.add_column("product_name", justify="left")
    table.add_column("description", justify="left")
    table.add_column("price", justify="right")
    table.add_column("quantity", justify="right")

    for product in user_products:
        table.add_row(str(product.id), str(product.user.id), product.name, product.description, str(int(product.minimum_sales_price)), str(product.quantity))
    console = Console()
    console.print(table)
    return user_products


def list_products_per_tag(tag_id):
    query = (Product
             .select()
             .join(ProductTag)
             .join(Tag)
             .where(Tag.id == tag_id))
    if query.exists():
        table = Table(title=f"List Products for tag_id: << {tag_id} >>", show_header=True, header_style="bold magenta")
        table.add_column("product_id", justify="right")
        table.add_column("user_id", justify="right")
        table.add_column("product_name", justify="left")
        table.add_column("description", justify="left")
        table.add_column("price", justify="right")
        table.add_column("quantity", justify="right")  
        for row in query:
            table.add_row(str(row.id), str(row.user_id), row.name, row.description, str(int(row.minimum_sales_price)), str(row.quantity))
        console = Console()
        console.print(table)
        return query
    else:
        print(f"Tag_id '{tag_id}' not found.")
        return f"Tag_id '{tag_id}' not found."


def add_product_to_catalog(user_id, product_name, description, minimum_sales_price, quantity, list_user_products = list_user_products):
    'requirements mention descripton, price and quantity as well, so I have added them to the function.'
    try:
        user = User.get(User.id == user_id)
    except DoesNotExist:
        print("User_id does not exist in table User.")
        return "User_id does not exist in table User."
    # Create product only for user, if it does not exist yet:
    product, created = Product.get_or_create(user=user, name=product_name, defaults={'description': description, 'minimum_sales_price': minimum_sales_price, 'quantity': quantity})
    if not created: # not created == product already exists
        product.quantity += quantity
        product.description = description
        product.minimum_sales_price = minimum_sales_price
        product.save()
    # show the result of adding the product to the catalog:
    list_user_products(user_id)
    return product 


def update_stock(product_id, name=None, description=None, minimum_sales_price=None, quantity=None, list_user_products = list_user_products):
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
    # show the result of adding the product to the catalog:
    list_user_products(product.user_id)
    return product


def show_all_transactions():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Transaction ID")
    table.add_column("User Payment Method ID")
    table.add_column("Product ID")
    table.add_column("Quantity")
    table.add_column("Price")
    table.add_column("Date")
    table.add_column("Time")
    transactions = Transaction.select().order_by(Transaction.id.desc())
    for transaction in transactions:
        table.add_row(
            str(transaction.id),
            str(transaction.user_payment_method),
            str(transaction.product),
            str(transaction.quantity),
            str(transaction.price),
            str(transaction.date),
            str(transaction.time)
        )
    console = Console()
    console.print(table)


def purchase_product(user_payment_method_id, product_id, price, quantity, show_all_transactions = show_all_transactions):
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
    Transaction.create( product=product, 
                        user_payment_method=user_payment_method, 
                        quantity=quantity, 
                        price=price, 
                        date=random_date(TRANSACTION_YEAR, TRANSACTION_WEEK), 
                        time=random_time(TRANSACTION_START_OF_DAY_HOUR, TRANSACTION_END_OF_DAY_HOUR))
    # show the result of purchasing a product:
    show_all_transactions()


def remove_product(product_id, list_user_products = list_user_products):
    try:
        product = Product.get(Product.id == product_id)
    except DoesNotExist:
        print("Product_id does not exist in table Product.")
        return "Product_id does not exist in table Product."
    if product.transactions.exists():
        print("Cannot delete product. There are transactions associated with this product.")
        return "Cannot delete product. There are transactions associated with this product."
    if product.product_tags.exists():
        print("There are tags associated with this product...let's delete them.")
        for product_tag in product.product_tags:
            product_tag.delete_instance()
    user_id = product.user_id
    print(f'user_id: {user_id}')
    product.delete_instance()
    print(f'user_id: {user_id}')
    # show the result of deleting the product from the catalog:
    list_user_products(user_id)
    return product


if __name__ == "__main__":
    main()