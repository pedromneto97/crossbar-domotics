from mongoengine import *


class Pattern(EmbeddedDocument):
    unit = StringField()
    name = StringField(required=True)


class SceneItemType(Document):
    name = StringField(required=True, unique=True)
    type = StringField(required=True, choices=['SENSOR', 'ACTUATOR'])
    patterns = EmbeddedDocumentListField(Pattern, required=True)
