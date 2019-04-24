from bson import json_util

from Domain.MongoDomain import *
from Domain.ResidenceDomain import add_room_to_residence
from Models.Room import Room


def get_room_by_alias(alias: str, with_type: bool = True, with_scenes: bool = True) -> Room or None:
    pipeline = []
    if with_type:
        pipeline.append(lookup('room_type', 'type'))
        pipeline.append(unwind('$type'))
    if with_scenes:
        pipeline.append(lookup('scene_item', 'scenes'))
        pipeline.append(unwind('$scenes'))
        pipeline.append(lookup('scene_item_type', 'scenes.type'))
        pipeline.append(unwind('$scenes.type'))
        pipeline.append(group([
            ('type', '$first', '$type'),
            ('name', '$first', '$name'),
            ('scenes', '$push', '$scenes')
        ]))
    if with_scenes or with_type:
        room = list(Room.objects(alias=alias).aggregate(*pipeline))
        return json_util.dumps(room[0]) if len(room) > 0 else None
    return Room.objects(alias=alias).first().to_json()


def insert_room(data: str, residence_id: str) -> Room:
    r = Room.from_json(data)
    r.save()
    add_room_to_residence(residence_id, r)
    return r
