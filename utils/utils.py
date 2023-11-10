import random
import datetime

# list of functions:
# connectProductsToTags(products, tags, NR_OF_TAGS_PER_PRODUCT_LOWER_BOUNDARY, NR_OF_TAGS_PER_PRODUCT_UPPER_BOUNDARY) -> list[list[str]]
# create_sample_data_product(product_range: int, nr_of_products_for_each_product: int) -> list[list[str]]
# create_sample_data_user(nr_of_users: int) -> list[list[str]]
# random_date(year: int, week: int) -> str
# random_time(transaction_start_of_day_hour, transaction_end_of_day_hour)



def connectProductsToTags(
    products: list[list[str]], 
    tags: list[list[str]], 
    NR_OF_TAGS_PER_PRODUCT_LOWER_BOUNDARY: int, 
    NR_OF_TAGS_PER_PRODUCT_UPPER_BOUNDARY: int) -> list[list[str]]:
    # if there are e.g. 4 tags, then I needs this: "tag_ids = [1,2,3,4]", 5 tag_ids: "tag_ids = [1,2,3,4,5]", etc.
    tag_ids = list(map(lambda x: tags.index(x) + 1, tags)) # possible to add tags later on, wthout breaking the code.
    # goal: for each user, assign a random number of payment methods:
    list_with_dicts = []
    for i in range(len(products)):
        list_with_dicts.append({'product_id': i + 1}) # 
        list_with_dicts[i]['tags'] = random.sample(tag_ids, random.randint(NR_OF_TAGS_PER_PRODUCT_LOWER_BOUNDARY, NR_OF_TAGS_PER_PRODUCT_UPPER_BOUNDARY))
    product_tags = []
    for product in list_with_dicts:
        for tag in product['tags']:
            product_tags.append([product['product_id'], tag])
    return product_tags

def connectUsersToPaymentMethods(
        users: list[list[str]], 
        payment_methods: list[list[str]], 
        NR_OF_PAYMENT_METHODS_PER_USER_LOWER_BOUNDARY: int, 
        NR_OF_PAYMENT_METHODS_PER_USER_UPPER_BOUNDARY: int) -> list[list[str]]:
    # if there are e.g. 4 payment methods, then I needs this: "payment_method_ids = [1,2,3,4]", 5 payment methods: "payment_method_ids = [1,2,3,4,5]", etc.
    payment_method_ids = [(payment_methods.index(sublist) + 1) for sublist in payment_methods] # possible to add paymentmethod later on, wthout breaking the code.
    # goal: for each user, assign a random number of payment methods:
    list_with_dicts = []
    for i in range(len(users)):
        list_with_dicts.append({'user_id': i + 1}) # 
        list_with_dicts[i]['payment_methods'] = random.sample(payment_method_ids, random.randint(NR_OF_PAYMENT_METHODS_PER_USER_LOWER_BOUNDARY, NR_OF_PAYMENT_METHODS_PER_USER_UPPER_BOUNDARY))
    user_paymentmethods = []
    for user in list_with_dicts:
        for payment_method in user['payment_methods']:
            user_paymentmethods.append([user['user_id'], payment_method])
    return user_paymentmethods

def create_sample_data_product(product_range: int, product_quantity: int, sample_product_names_with_descriptions: list, NR_OF_USERS: int) -> list[list[str]]:
    users = []
    for i in range(product_range):
        '''
        To make data easier to read and understand, I made the minimum_sales_price the same nr as the product_id.
        '''
        user = {
            "user_id": f"{random.randint(1, NR_OF_USERS)}", 
            "name": f"{sample_product_names_with_descriptions[i][0]}", 
            "description": f"{sample_product_names_with_descriptions[i][1]}",
            "minimum_sales_price": f"{round((i + 1), 2)}", 
            "quantity":f"{product_quantity}",
        }
        users.append(user)
    return users

def create_sample_data_user(nr_of_users: int) -> list[list[str]]:
    users = []
    for i in range(nr_of_users):
        user = {
            "last_name": f"last_name_{i + 1}",
            "first_name": f"first_name_{i + 1}",
            "phone_number": f"{i + 1}",
            "email": f"email_{i + 1}@example.com",
            "street":f"street_{i + 1}",
            "house_number": f"{i + 1}",
            "postal_code": f"postal_code_{i + 1}",
            "city": f"city_{i}",
            "country": f"country_{i + 1}",
            "password":f"password_{i + 1}",
        }
        users.append(user)
    return users

def levenshtein_distance(s1: str, s2: str) -> int:
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

def random_date(year: int, week: int) -> str:
    first_day = datetime.datetime.strptime(f'{year}-W{week}-1', '%G-W%V-%u').date()
    random_day = first_day + datetime.timedelta(days=random.randint(0, 6))
    return random_day.strftime('%Y-%m-%d')


def random_time(transaction_start_of_day_hour: int, transaction_end_of_day_hour: int) -> str:
    hour = random.randint(transaction_start_of_day_hour, transaction_end_of_day_hour)
    minute = random.randint(0, 59)
    return datetime.time(hour=hour, minute=minute).strftime('%H:%M')

def remove_duplicates(result: list[list[str]]):
    seen = set()
    result_no_duplicates = []
    for item in result:
        if item[0] not in seen:
            seen.add(item[0])
            result_no_duplicates.append(item)
    return result_no_duplicates