from bson import json_util

from Models.SceneItemType import SceneItemType, Pattern


def get_scene_item_type_by_type(type: str) -> SceneItemType or None:
    sit = SceneItemType.objects(type=type).first()
    return sit if sit is not None else None


def insert_scene_item_type(data: str) -> SceneItemType:
    sit = SceneItemType.from_json(data)
    sit.save()
    return sit


def edit_scene_item_type(_id: str, data: str):
    sit: SceneItemType = SceneItemType.objects(_id=_id).first()
    data: dict = json_util.loads(data)
    if 'patterns' in data:
        data.pop('patterns')
    for key, item in data.items():
        setattr(sit, key, item)
    sit.save()


def add_pattern(_id: str, unit: str, name: str):
    p: Pattern = Pattern(unit=unit, name=name)
    SceneItemType.objects(_id=_id).update_one(push__patterns=p)


def remove_pattern(_id: str, unit: str, name: str):
    p: Pattern = Pattern(unit=unit, name=name)
    SceneItemType.objects(_id=_id).update_one(pull__patterns=p)


def delete_scene_item_type(_id: str):
    SceneItemType.objects(_id=_id).delete()
