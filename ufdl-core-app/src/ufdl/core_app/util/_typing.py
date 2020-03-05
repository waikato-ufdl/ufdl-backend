"""
Module for types used by the UFDL backend.
"""
from typing import Union, List, Dict

# The type of a query-parameter value
QueryParameterValue = Union[str, List[str]]

# The type of a set of query parameters
QueryParameters = Dict[str, QueryParameterValue]
