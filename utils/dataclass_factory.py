def as_dict_remove_none(data):
    """
    A custom dict_factory for dataclasses.asdict that removes items where the value is None.
    Useful for creating clean API query parameters.
    """
    return dict((key, value) for key, value in data if value is not None)
