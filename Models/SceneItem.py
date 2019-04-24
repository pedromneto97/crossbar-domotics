from mongoengine import *

from Models.SceneItemType import SceneItemType


class SceneItem(Document):
    name = StringField(required=True)
    pattern = IntField(required=True, min_value=0)
    icon = StringField()
    type = ReferenceField(SceneItemType, reverse_delete_rule=DENY, required=True)
    active = BooleanField(default=True)
