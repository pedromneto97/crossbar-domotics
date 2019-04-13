from typing import List

from mongoengine import InvalidQueryError

LOOKUP = 1
UNWIND = 2


def pipeline(operator: int = 0, **kwargs) -> dict:
    if operator is LOOKUP:
        if check_kwargs(['from_collection', 'local_field', 'foreign_field'], kwargs):
            return lookup(kwargs['from_collection'], kwargs['local_field'], kwargs['foreign_field'],
                          kwargs['local_field'] if 'as_field' not in kwargs.keys() else kwargs['as_field'])
        raise InvalidQueryError
    if operator is UNWIND:
        if check_kwargs(['path', 'local_field', 'foreign_field'], kwargs):
            return lookup(kwargs['from_collection'], kwargs['local_field'], kwargs['foreign_field'],
                          kwargs['local_field'] if 'as_field' not in kwargs.keys() else kwargs['as_field'])
        raise InvalidQueryError


def lookup(from_collection: str, local_field: str, foreign_field: str, as_field: str = None):
    return {
        '$lookup': {
            'from': from_collection,
            'localField': local_field,
            'foreignField': foreign_field,
            'as': as_field
        }
    }


def unwind(path: str, preserve_null_and_empty_arrays: bool = True, include_array_index: str = None):
    uw = {
        '$unwind': {
            'path': path,
            'preserveNullAndEmptyArrays': preserve_null_and_empty_arrays,
        }
    }
    if include_array_index is not None:
        uw['$unwind'].update({'includeArrayIndex': include_array_index})
    return uw


def check_kwargs(keys: List[str], kwargs):
    for key in keys:
        if key not in kwargs.keys():
            return False
    return True
