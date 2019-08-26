from autobahn.wamp.auth import derive_key

from mongoengine import *


class User(Document):
    username = StringField(required=True, unique=True)
    name = StringField(required=True)
    password = StringField(required=True)
    cpf = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    default_residence = ObjectIdField(null=True)

    @staticmethod
    def encrypt(password: str, salt: str = None) -> bytes:
        return derive_key(password, salt)
