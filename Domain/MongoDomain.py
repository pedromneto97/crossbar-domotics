from typing import List, Tuple


def lookup(from_collection: str, local_field: str, foreign_field: str = '_id', as_field: str = None) -> dict:
    return {
        '$lookup': {
            'from': from_collection,
            'localField': local_field,
            'foreignField': foreign_field,
            'as': as_field if as_field is not None else local_field
        }
    }


def unwind(path: str, preserve_null_and_empty_arrays: bool = True, include_array_index: str = None) -> dict:
    uw = {
        '$unwind': {
            'path': path,
            'preserveNullAndEmptyArrays': preserve_null_and_empty_arrays,
        }
    }
    if include_array_index is not None:
        uw['$unwind'].update({'includeArrayIndex': include_array_index})
    return uw


# id of the group and list of tuples (field, accumulator, expression)
def group(tuple_array: List[Tuple[str, str, str]], _id='_id') -> dict:
    gp = {
        '$group': {
            '_id': _id
        }
    }
    for field, accumulator, expression in tuple_array:
        gp['$group'].update({
            field: {
                accumulator: expression
            }
        })
    return gp
