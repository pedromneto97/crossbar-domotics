from typing import List

from Models.ResidenceType import ResidenceType


def get_residence_types() -> List[ResidenceType]:
    return ResidenceType.objects()


def get_residence_type(type: str) -> ResidenceType:
    rt = ResidenceType.objects(type=type).first()
    return rt if rt is not None else None


def create_residence_type(data: str):
    rt = ResidenceType.from_json(data)
    rt.save()


def edit_residence_type(_id: str, data: str):
    rt = ResidenceType.objects(_id=_id).first()
    data = json_util.loads(data)
    for key, item in data.items():
        setattr(r, key, item)
    rt.save()


def remove_residence_type(_id: str):
    ResidenceType.objects(_id=_id).delete()
