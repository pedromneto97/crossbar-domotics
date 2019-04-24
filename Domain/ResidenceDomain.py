from Models.Residence import Residence
from Models.Room import Room


def add_room_to_residence(_id: str, room: Room):
    Residence.objects(_id=_id).update_one(push__rooms=room)
