"""
Module for types used by the UFDL backend.
"""
from typing import Union, List, Dict

# The type of a query-parameter value
QueryParameterValue = Union[str, List[str]]

# The type of a set of query parameters
QueryParameters = Dict[str, QueryParameterValue]


def is_query_parameters(value) -> bool:
    """
    Checks if a value is a dictionary of query parameters.

    :param value:   The value to check.
    :return:        True if the value is a dictionary of query parameters,
                    False if not.
    """
    # The value must be a dictionary
    if not isinstance(value, dict):
        return False

    # Each entry must be a string -> query parameter value
    for key, item in value.items():
        if not isinstance(key, str):
            return False

        if not is_query_parameter_value(item):
            return False

    return True


def is_query_parameter_value(value) -> bool:
    """
    Checks if a value is a query parameter value.

    :param value:   The value to check.
    :return:        True if the value is a query parameter value,
                    False if not.
    """
    # Must be a string or list of strings
    return isinstance(value, str) or (isinstance(value, list) and all(map(lambda sub: isinstance(sub, str), value)))
