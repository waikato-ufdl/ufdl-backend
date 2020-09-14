"""
Utility filters/aggregates for query-sets.
"""
from django.db import models


def max_value(query_set: models.QuerySet, field_name: str, default=None):
    """
    Returns the maximum value of a field in a query-set.

    :param query_set:   The query-set to aggregate.
    :param field_name:  The name of the field to find the maximum value for.
    :param default:     The value to return if the query-set is empty.
    :return:            The maximum value for the field, or default if empty.
    """
    # Handle the default case
    if not query_set.exists():
        return default

    return query_set.aggregate(models.Max(field_name))[f'{field_name}__max']
