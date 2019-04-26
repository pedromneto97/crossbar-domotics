from mongoengine import *

from Models.SceneItemType import SceneItemType


class Scene(EmbeddedDocument):
    scene = ReferenceField(SceneItemType)
    pins = ListField(choices=[])


class Controller(Document):
    mac = StringField(required=True, unique=True)
    scenes = ListField(ReferenceField(SceneItemType, reverse_delete_rule=DENY))
