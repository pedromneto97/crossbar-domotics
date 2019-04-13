from typing import List

from bson import json_util

from Domain.MongoDomain import *
from Models.Residence import Residence


def get_residences(user_id: str, with_city: bool = True, with_type: bool = True) -> List[Residence]:
    pipeline = []
    if with_city:
        pipeline.append(lookup('residence_type', 'type'))
        pipeline.append(unwind('$type'))
    if with_type:
        pipeline.append(lookup('address', 'address.postal_code'))
        pipeline.append(unwind('$address.postal_code'))
    if with_type or with_city:
        return json_util.dumps(Residence.objects(users=user_id).aggregate(*pipeline))
    return Residence.objects(users=user_id).to_json()


def get_residence(_id: str) -> Residence or None:
    residence = Residence.objects(_id=_id).first()
    return None if residence is None else residence.to_json()


def get_residence_by_alias(alias: str, with_city: bool = True, with_type: bool = True,
                           with_rooms: bool = True) -> Residence or None:
    pipeline = []
    if with_city:
        pipeline.append(lookup('residence_type', 'type'))
        pipeline.append(unwind('$type'))
    if with_type:
        pipeline.append(lookup('address', 'address.postal_code'))
        pipeline.append(unwind('$address.postal_code'))
    if with_rooms:
        pipeline.append(lookup('room', 'rooms'))
        pipeline.append(unwind('$rooms'))
    if with_rooms or with_city or with_type:
        return json_util.dumps(list(Residence.objects(alias=alias).aggregate(*pipeline))[0])
    return Residence.objects(users=alias).first().to_json()


def edit_residence(_id: str, postal_code: str = None, district: str = None, street: str = '', number: int = -1,
                   complement: str = '', users: List[str] = None, rooms: List[str] = None, type: str = '',
                   name: str = '') -> bool:
    residence = get_residence(_id)
    if postal_code is not None:
        residence.address.postal_code = postal_code
    if district is not None:
        residence.address.district = district
