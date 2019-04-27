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


def get_controller(_id: str) -> Controller or None:
    si: Controller = Controller.objects(_id=_id).first()
    return si if si is not None else None


def insert_controller(data: str) -> Controller:
    c: Controller = Controller.from_json(data)
    c.save()
    return c


def edit_controller(_id: str, data: str):
    c: Controller = Controller.objects(_id=_id).first()
    data: dict = json_util.loads(data)
    if 'scene' in data:
        data.pop('scene')
    for key, item in data.items():
        setattr(c, key, item)
    c.save()


def delete_controller(_id: str):
    Controller.objects(_id=_id).delete()
