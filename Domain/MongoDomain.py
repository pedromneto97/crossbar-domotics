def lookup(from_collection: str, local_field: str, foreign_field: str, as_field: str = None):
    return {
        '$lookup': {
            'from': from_collection,
            'localField': local_field,
            'foreignField': foreign_field,
            'as': as_field if as_field is not None else local_field
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
