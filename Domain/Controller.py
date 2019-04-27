from bson import json_util

from Domain.MongoDomain import *
from Models.Controller import Controller


def get_config(mac: str) -> Controller:
    pipeline = []
    pipeline.append(unwind('$scenes'))
    pipeline.append(lookup('scene_item', 'scenes.scene'))
    pipeline.append(unwind('$scenes.scene'))
    pipeline.append(lookup('scene_item_type', 'scenes.scene.type'))
    pipeline.append(unwind('$scenes.scene.type'))
    pipeline.append(group([
        ('mac', '$first', '$mac'),
        ('type', '$first', '$type'),
        ('scenes', '$push', '$scenes'),
    ]))
    residence = list(Controller.objects(mac=mac).aggregate(*pipeline))
    return json_util.dumps(residence[0]) if len(residence) > 0 else None
