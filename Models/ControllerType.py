from mongoengine import *


class Pins(EmbeddedDocument):
    pin = IntField(min_value=0)
    functions = ListField(StringField())


class ControllerType(Document):
    name = StringField()
    model = StringField(required=True)
    available_pins = EmbeddedDocumentListField(Pins, required=True)
