from typing import List

from bson import json_util

from Models.Residence import Residence


def get_residences(user_id: str, with_city: bool = True, with_type: bool = True) -> List[Residence]:
    pipeline = []
    if with_city:
        pipeline.append({
            '$lookup': {
                'from': 'residence_type',
                'localField': 'type',
                'foreignField': '_id',
                'as': 'type'
            }
        })
        pipeline.append({
            '$unwind': {
                'path': '$type',
                'preserveNullAndEmptyArrays': True
            }
        })
    if with_type:
        pipeline.append({
            '$lookup': {
                'from': 'address',
                'localField': 'address.postal_code',
                'foreignField': '_id',
                'as': 'address.postal_code'
            }
        })
        pipeline.append({
            '$unwind': {
                'path': '$address.postal_code',
                'preserveNullAndEmptyArrays': True
            }
        })
    if with_type or with_city:
        return json_util.dumps(Residence.objects(users=user_id).aggregate(*pipeline))
    return Residence.objects(users=user_id).to_json()


def get_residence(_id: str) -> Residence or None:
    residence = Residence.objects(_id=_id).first()
    return None if residence is None else residence.to_json()


def get_residence_by_alias(alias: str, with_city: bool = True, with_type: bool = True,
                           with_rooms: bool = True) -> Residence or None:
    residence = Residence.objects(alias=alias).first()
    return None if residence is None else residence.to_json()


def edit_residence(_id: str, postal_code: str = None, district: str = None, street: str = '', number: int = -1,
                   complement: str = '', users: List[str] = None, rooms: List[str] = None, type: str = '',
                   name: str = '') -> bool:
    residence = get_residence(_id)
    if postal_code is not None:
        residence.address.postal_code = postal_code
    if district is not None:
        residence.address.district = district
