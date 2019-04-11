from mongoengine import *

from Models.Address import Address as Postal_Code
from Models.ResidenceType import ResidenceType
from Models.Room import Room
from Models.User import User


class Address(EmbeddedDocument):
    postal_code = ReferenceField(Postal_Code, required=True)
    district = StringField(required=True)
    street = StringField(required=True)
    number = IntField(required=True, min_value=0)
    complement = StringField()


class Residence(Document):
    users = ListField(ReferenceField(User, reverse_delete_rule=PULL), required=True)
    rooms = ListField(ReferenceField(Room, reverse_delete_rule=PULL), required=True)
    type = ReferenceField(ResidenceType, reverse_delete_rule=DENY, required=True)
    name = StringField(required=True)
    address = EmbeddedDocumentField(Address, required=True)
    alias = StringField(required=True, unique=True)
    icon = StringField()
