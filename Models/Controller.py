from mongoengine import *

from Models.ControllerType import ControllerType
from Models.SceneItemType import SceneItemType


class Scene(EmbeddedDocument):
    scene = ReferenceField(SceneItemType)
    pins = ListField(IntField())


class Controller(Document):
    mac = StringField(required=True, unique=True)
    scenes = EmbeddedDocumentListField(Scene, required=True)
    type = ReferenceField(ControllerType, required=True, reverse_delete_rule=DENY)
