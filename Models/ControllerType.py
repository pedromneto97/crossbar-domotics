from mongoengine import *


class ControllerType(Document):
    name = StringField(required=True)
    available_pins = ListField(IntField(), required=True)
