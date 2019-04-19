from mongoengine import *


class RoomType(Document):
    type = StringField(required=True, unique=True)
    icon = StringField(required=True)
