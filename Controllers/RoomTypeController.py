from typing import List

from Models.RoomType import RoomType


def get_room_types() -> List[RoomType]:
    return RoomType.objects()


def get_room_type(type: str) -> RoomType:
    rt = RoomType.objects(type=type).first()
    return rt if rt is not None else None


def create_room_type(data: str):
    rt = RoomType.from_json(data)
    rt.save()


def edit_room_type(_id: str, data: str):
    rt = RoomType.objects(_id=_id).first()
    data = json_util.loads(data)
    for key, item in data.items():
        setattr(r, key, item)
    rt.save()


def remove_room_type(_id: str):
    RoomType.objects(_id=_id).delete()
