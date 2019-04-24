from Models.SceneItemType import SceneItemType


def get_scene_item_type_by_type(type: str) -> SceneItemType or None:
    sit = SceneItemType.objects(type=type).first()
    return sit if sit is not None else None


def insert_scene_item_type(data: str) -> SceneItemType:
    sit = SceneItemType.from_json(data)
    sit.save()
    return sit


def edit_scene_item_type(_id: str, data: str):
    sit: SceneItemType = SceneItemType.objects(_id=_id).first()
    sit.from_json(data)
    sit.save()


def delete_scene_item_type(_id: str):
    SceneItemType.objects(_id=_id).delete()
