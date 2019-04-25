from bson import json_util

from Models.SceneItem import SceneItem


def get_scene_item(_id: str) -> SceneItem or None:
    si: SceneItem = SceneItem.objects(_id=_id).first()
    return si if si is not None else None


def insert_scene_item(data: str) -> SceneItem:
    si: SceneItem = SceneItem.from_json(data)
    si.save()
    return si


def edit_scene_item(_id: str, data: str):
    si: SceneItem = SceneItem.objects(_id=_id).first()
    data: dict = json_util.loads(data)
    for key, item in data.items():
        setattr(si, key, item)
    si.save()


def disable_scene_item(_id: str):
    SceneItem.objects(_id=_id).update_one(set__active=False)
