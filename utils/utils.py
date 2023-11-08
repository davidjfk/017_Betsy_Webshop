import random
import datetime

# list of functions:
# assign_tags(products, tags, nr_of_tags_per_product_lower_boundary, nr_of_tags_per_product_upper_boundary)
# create_sample_data_product(product_range: int, nr_of_products_for_each_product: int) -> list[list[str]]
# create_sample_data_user(nr_of_users: int) -> list[list[str]]
# random_date(year: int, week: int) -> str
# random_time(transaction_start_of_day_hour, transaction_end_of_day_hour)



def assign_tags(products, tags, nr_of_tags_per_product_lower_boundary, nr_of_tags_per_product_upper_boundary):
    for product in products:
        product['tags'] = random.sample(tags, random.randint(nr_of_tags_per_product_lower_boundary, nr_of_tags_per_product_upper_boundary))
    return products


def connectProductsToTags(
    products, 
    tags, 
    NR_OF_TAGS_PER_PRODUCT_LOWER_BOUNDARY, 
    NR_OF_TAGS_PER_PRODUCT_UPPER_BOUNDARY):
    # if there are e.g. 4 tags, then I needs this: "tag_ids = [1,2,3,4]", 5 tag_ids: "tag_ids = [1,2,3,4,5]", etc.
    tag_ids = list(map(lambda x: tags.index(x) + 1, tags)) # possible to add tags later on, wthout breaking the code.
    # goal: for each user, assign a random number of payment methods:
    list_with_dicts = []
    for i in range(len(products)):
        list_with_dicts.append({'product_id': i + 1}) # 
        list_with_dicts[i]['tags'] = random.sample(tag_ids, random.randint(NR_OF_TAGS_PER_PRODUCT_LOWER_BOUNDARY, NR_OF_TAGS_PER_PRODUCT_UPPER_BOUNDARY))
    # print('list with dicts:')
    # print(list_with_dicts)
    product_tags = []
    for product in list_with_dicts:
        for tag in product['tags']:
            product_tags.append([product['product_id'], tag])
    return product_tags

def connectUsersToPaymentMethods(
        users, 
        payment_methods, 
        NR_OF_PAYMENT_METHODS_PER_USER_LOWER_BOUNDARY, 
        NR_OF_PAYMENT_METHODS_PER_USER_UPPER_BOUNDARY):
    # if there are e.g. 4 payment methods, then I needs this: "payment_method_ids = [1,2,3,4]", 5 payment methods: "payment_method_ids = [1,2,3,4,5]", etc.
    payment_method_ids = [(payment_methods.index(sublist) + 1) for sublist in payment_methods] # possible to add paymentmethod later on, wthout breaking the code.
    # goal: for each user, assign a random number of payment methods:
    list_with_dicts = []
    for i in range(len(users)):
        list_with_dicts.append({'user_id': i + 1}) # 
        list_with_dicts[i]['payment_methods'] = random.sample(payment_method_ids, random.randint(NR_OF_PAYMENT_METHODS_PER_USER_LOWER_BOUNDARY, NR_OF_PAYMENT_METHODS_PER_USER_UPPER_BOUNDARY))
    # print(user_list)
    user_paymentmethods = []
    for user in list_with_dicts:
        for payment_method in user['payment_methods']:
            user_paymentmethods.append([user['user_id'], payment_method])
    # print(user_paymentmethods)
    return user_paymentmethods

def create_sample_data_product(product_range: int, product_quantity: int, sample_product_names_with_descriptions: list, NR_OF_USERS: int) -> list[list[str]]:
    users = []
    for i in range(product_range):
        user = {
            "user_id": f"{random.randint(1, NR_OF_USERS)}", 
            # random user_id makes fn more difficult to test.
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


def random_date(year: int, week: int) -> str:
    first_day = datetime.datetime.strptime(f'{year}-W{week}-1', '%G-W%V-%u').date()
    random_day = first_day + datetime.timedelta(days=random.randint(0, 6))
    return random_day.strftime('%Y-%m-%d')


def random_time(transaction_start_of_day_hour: int, transaction_end_of_day_hour: int) -> str:
    hour = random.randint(transaction_start_of_day_hour, transaction_end_of_day_hour)
    minute = random.randint(0, 59)
    return datetime.time(hour=hour, minute=minute).strftime('%H:%M')