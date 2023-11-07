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
        product['tags'] = random.sample(tags, random.randint(2, 6))
    return products

def create_sample_data_product(product_range: int, nr_of_products_for_each_product: int) -> list[list[str]]:
    users = []
    for i in range(product_range):
        user = {
            "user_id": f"{i + 1}", 
            # random user_id makes fn more difficult to test.
            "name": f"product_name_{i + 1}", 
            "description": f"product_description_{i + 1}",
            "minimum_sales_price": f"{round((i + 1), 2)}",
            "quantity":f"{nr_of_products_for_each_product}",
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