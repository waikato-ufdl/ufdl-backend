from typing import List

from django.db.models import QuerySet
from django.db.models.expressions import OrderBy as DjangoOrderBy, F

from ufdl.json.core.filter import OrderBy

from wai.json.object import Absent


def order_by(query_set: QuerySet, by: List[OrderBy]) -> QuerySet:
    """
    Applies an order-by specification to a query-set.

    :param query_set:   The query-set to order.
    :param by:          The specification of how to order the query-set.
    :return:            The ordered query-set.
    """
    return query_set.order_by(*map(expression_from_order_by, by))


def expression_from_order_by(by: OrderBy) -> DjangoOrderBy:
    """
    Converts a JSON order-by specification into an actual ordering
    expression.

    :param by:  The order-by specification.
    :return:    The order-by expression.
    """
    # Create the argument to supply to the ordering regarding null values
    nulls_kwarg = {"nulls_first": by.nulls_first} if by.nulls_first is not Absent else {}

    # Create a value reference
    expression = F(by.field)

    # Get the ascending/descending generator
    generator = expression.asc if by.ascending else expression.desc

    return generator(**nulls_kwarg)
