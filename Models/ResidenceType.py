from mongoengine import *


class ResidenceType(Document):
    type = StringField(required=True, unique=True)
    icon = StringField(required=True)
