from Models.SensorType import SensorType
from mongoengine import *


class Sensor(Document):
    name = StringField(required=True)
    pattern = IntField(required=True, min_value=0)
    icon = StringField(required=True)
    type = ReferenceField(SensorType, reverse_delete_rule=DENY, required=True)
