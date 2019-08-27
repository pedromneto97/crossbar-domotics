from autobahn.wamp import CallDetails
from bson import json_util

from Domain.MongoDomain import *
from Models.Residence import Residence
from Models.User import User


def get_residences(with_city: bool = True, with_type: bool = True, **kwargs) -> List[Residence]:
    details = kwargs.get('details')  # type: CallDetails
    pipeline = []
    if with_type:
        pipeline.append(lookup('residence_type', 'type'))
        pipeline.append(unwind('$type'))
    if with_city:
        pipeline.append(lookup('address', 'address.postal_code'))
        pipeline.append(unwind('$address.postal_code'))
    if with_type or with_city:
        return json_util.dumps(Residence.objects(users=details.caller_authid).aggregate(*pipeline))
    return Residence.objects(users=details.caller_authid).to_json()


def get_residence(_id: str) -> Residence or None:
    residence = Residence.objects(_id=_id).first()
    return None if residence is None else residence.to_json()


def get_residence_by_alias(alias: str, with_city: bool = True, with_type: bool = True,
                           with_rooms: bool = True, with_users: bool = False) -> Residence or None:
    pipeline = []
    if with_city:
        pipeline.append(lookup('address', 'address.postal_code'))
        pipeline.append(unwind('$address.postal_code'))
    if with_type:
        pipeline.append(lookup('residence_type', 'type'))
        pipeline.append(unwind('$type'))
    if with_users:
        pipeline.append(lookup('user', 'users'))
    if with_rooms:
        pipeline.append(lookup('room', 'rooms'))
        pipeline.append(unwind('$rooms'))
        pipeline.append(lookup('room_type', 'rooms.type'))
        pipeline.append(unwind('$rooms.type'))
        pipeline.append(group([
            ('users', '$first', '$users'),
            ('type', '$first', '$type'),
            ('name', '$first', '$name'),
            ('address', '$first', '$address'),
            ('rooms', '$push', '$rooms'),
            ('alias', '$first', '$alias')
        ]))
    if with_rooms or with_city or with_type or with_users:
        residence = list(Residence.objects(alias=alias).aggregate(*pipeline))
        return json_util.dumps(residence[0]) if len(residence) > 0 else None
    return Residence.objects(alias=alias).first().to_json()


def create_residence(data):
    r: Residence = Residence.from_json(data)
    r.save()


def edit_residence(_id: str, data: str):
    r: Residence = Residence.objects(_id=_id).first()
    data: dict = json_util.loads(data)
    if 'address' in data:
        for key, item in data.get('address').items():
            setattr(r.address, key, item)
        data.pop('address')
    for key, item in data.items():
        setattr(r, key, item)
    r.save()


def delete_residence(_id: str):
    Residence.objects(_id=_id).delete()


def add_user_to_residence(_id: str, user_id: str):
    u = User.objects(_id=user_id).first()
    Residence.objects(_id=_id).update_one(push__users=u)
