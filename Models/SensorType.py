from mongoengine import *


class Pattern(EmbeddedDocument):
    unit = StringField(required=True)
    name = StringField(required=True)


class SensorType(Document):
    type = StringField(required=True, unique=True)
    patterns = EmbeddedDocumentListField(Pattern, required=True)
