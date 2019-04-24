from Models.SceneItem import SceneItem


def get_scene_item(_id: str) -> SceneItem or None:
    si = SceneItem.objects(_id=_id).first()
    return si if si is not None else None


def insert_scene_item(data: str) -> SceneItem:
    si = SceneItem.from_json(data)
    si.save()
    return si


def edit_scene_item(_id: str, data: str):
    si = SceneItem.objects(_id=_id).first()
    si.from_json(data)
    si.save()


def disable_scene_item(_id: str):
    SceneItem.objects(_id=_id).update_one(set__active=False)
