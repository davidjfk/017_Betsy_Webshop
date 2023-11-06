# Models go here
from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateField,
    TextField,
    DecimalField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TimeField,
)

db = SqliteDatabase("database.db")

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = AutoField()
    last_name = CharField()
    first_name = CharField()
    phone_number = TextField() # length of phone number is variable
    email = CharField(unique=True)
    street = CharField()
    house_number = CharField() # house number can contain letters
    postal_code = CharField()
    city = CharField()
    country = CharField()
    password = CharField()


class Product(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="products")
    name = CharField()
    description = TextField()
    price = DecimalField()
    available = BooleanField()

class PaymentMethod(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="payment_methods")
    name = CharField()
    description = TextField()
    active = BooleanField()
    fee = CharField() # percentage, e.g. 0.01 = 1% // amount: 1.00 = 1 euro, 0.50 = 50 cents // "no extra costs"

class Transaction(BaseModel):
    id = AutoField()
    payment_method = ForeignKeyField(PaymentMethod, backref="transactions") # backref: get all transactions for this payment method
    product = ForeignKeyField(Product, backref="transactions") # backref: get all transactions for this product
    User = ForeignKeyField(User, backref="transactions") # backref: get all transactions for this user
    quantity = IntegerField()
    price = DecimalField()
    date = DateField()
    time = TimeField()

class Tag(BaseModel):
    id = AutoField()
    name = CharField()

class ProductTag(BaseModel):
    id = AutoField()
    product = ForeignKeyField(Product, backref="product_tags") # backref: get all producttags for this product
    tag = ForeignKeyField(Tag, backref="product_tags") # backref: get all producttags for this tag


