from mongoengine import *


class RoomType(Document):
    type = StringField(required=True, unique=True)
