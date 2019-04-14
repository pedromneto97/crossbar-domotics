from bson import json_util

from Domain.MongoDomain import *
from Models.Room import Room


def get_room_by_alias(alias: str, with_type: bool = True, with_scenes: bool = True) -> Room or None:
    pipeline = []
    if with_type:
        pipeline.append(lookup('room_type', 'type'))
        pipeline.append(unwind('$type'))
    if with_scenes:
        pipeline.append(lookup('sensor', 'scenes'))
        pipeline.append(unwind('$scenes'))
        pipeline.append(lookup('sensor_type', 'scenes.type'))
        pipeline.append(unwind('$scenes.type'))
        pipeline.append(group([
            ('type', '$first', '$type'),
            ('name', '$first', '$name'),
            ('address', '$first', '$address'),
            ('scenes', '$push', '$scenes')
        ]))
    if with_scenes or with_type:
        room = list(Room.objects(alias=alias).aggregate(*pipeline))
        return json_util.dumps(room[0]) if len(room) > 0 else None
    return Room.objects(alias=alias).first().to_json()
