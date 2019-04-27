from mongoengine import *


class ControllerType(Document):
    name = StringField()
    model = StringField(required=True)
    available_pins = ListField(IntField(), required=True)
