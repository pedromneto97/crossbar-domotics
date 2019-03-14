from mongoengine import *
from Models.Sensor import Sensor


class Measurement(document):
    value = IntField(required=True)
    timestamp = DateTimeField(required=True)
    sensor = ReferenceField(Sensor, reverse_delete_rule=DENY)
