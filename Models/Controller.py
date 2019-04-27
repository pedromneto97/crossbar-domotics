from mongoengine import *

from Models.ControllerType import ControllerType
from Models.SceneItem import SceneItem


class Scene(EmbeddedDocument):
    scene = ReferenceField(SceneItem, unique=True)
    pins = ListField(IntField(min_value=0))


class Controller(Document):
    mac = StringField(required=True, unique=True)
    scenes = EmbeddedDocumentListField(Scene, required=True)
    type = ReferenceField(ControllerType, required=True, reverse_delete_rule=DENY)
