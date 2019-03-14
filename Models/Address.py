from mongoengine import *


class Address(Document):
    postal_code = StringField(required=True, regex='^[0-9]{8}$', unique=True)
    province = StringField(required=True)
    country = StringField(required=True)
