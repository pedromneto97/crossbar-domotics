from typing import List

from Models.Residence import Residence


def get_residences(user_id: str) -> List[Residence]:
    return Residence.objects(users=user_id).to_json()


def get_residence(_id: str) -> Residence or None:
    residence = Residence.objects(_id=_id).first()
    return None if residence is None else residence.to_json()


def edit_residence(_id: str, postal_code: str = None, district: str = None, street: str = '', number: int = -1,
                   complement: str = '', users: List[str] = None, rooms: List[str] = None, type: str = '',
                   name: str = '') -> bool:
    residence = get_residence(_id)
    if postal_code is not None:
        residence.address.postal_code = postal_code
    if district is not None:
        residence.address.district = district
