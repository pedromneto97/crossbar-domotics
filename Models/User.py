import hashlib

from mongoengine import *

from Models.Residence import Residence


class User(Document):
    username = StringField(required=True, unique=True)
    name = StringField(required=True)
    password = StringField(required=True)
    cpf = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    default_residence = ReferenceField(Residence, reverse_delete_rule=PULL)

    @staticmethod
    def encrypt(password: str, salt: str = None) -> str:
        a = hashlib.sha1()
        b = hashlib.sha1()
        a.update(password.encode('utf-8'))
        aux = ''
        if salt is not None:
            aux = salt
        b.update((str(a.hexdigest()) + aux).encode('utf-8'))
        return str(b.hexdigest())
