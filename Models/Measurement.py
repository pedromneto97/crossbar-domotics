from mongoengine import *

from Models.SceneItem import SceneItem


class Measurement(Document):
    value = FloatField(required=True)
    timestamp = DateTimeField(required=True)
    sensor = ReferenceField(SceneItem, reverse_delete_rule=DENY)
