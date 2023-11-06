def create_sample_data_product(n: int) -> list[list[str]]:
    users = []
    for i in range(n):
        user = {
            "user_id": f"{i + 1}", 
            # random user_id makes fn more difficult to test.
            "name": f"product_name_{i + 1}", 
            "description": f"product_description_{i + 1}",
            "price": f"{round((i + 1), 2)}",
            "quantity":f"{i + 1}",
        }
        users.append(user)
    return users

def create_sample_data_user(n: int) -> list[list[str]]:
    users = []
    for i in range(n):
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