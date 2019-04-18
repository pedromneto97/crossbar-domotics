from mongoengine import *

from Models.SceneItem import SceneItem


class Measurement(document):
    value = IntField(required=True)
    timestamp = DateTimeField(required=True)
    sensor = ReferenceField(SceneItem, reverse_delete_rule=DENY)
