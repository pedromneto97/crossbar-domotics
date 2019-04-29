from mongoengine import *

from Models.RoomType import RoomType
from Models.SceneItem import SceneItem


class Room(Document):
    type = ReferenceField(RoomType, reverse_delete_rule=DENY, required=True)
    name = StringField(required=True)
    scenes = ListField(ReferenceField(SceneItem, reverse_delete_rule=PULL), unique=True)
    icon = StringField(required=True)
    alias = StringField(required=True, unique=True)
