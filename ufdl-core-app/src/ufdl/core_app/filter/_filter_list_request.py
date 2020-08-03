from django.db.models import QuerySet

from simple_django_teams.mixins import SoftDeleteQuerySet

from ufdl.json.core.filter import FilterSpec

from wai.json.object import Absent

from ..models import User
from ._generate_qs import generate_qs
from ._order_by import order_by


def filter_list_request(query_set: QuerySet, filter_spec: FilterSpec) -> QuerySet:
    """
    Filters a list request based on the given filter-spec.

    :param query_set:       The query-set representing the unfiltered list.
    :param filter_spec:     A filter-spec object specifying how to filter.
    :return:                The filtered query-set.
    """
    # If filter expressions are provided, filter by them
    if filter_spec.expressions is not Absent:
        for q in generate_qs(filter_spec.expressions):
            query_set = query_set.filter(q)

    # If order-by expressions are provided, order by them
    if filter_spec.order_by is not Absent:
        query_set = order_by(query_set, filter_spec.order_by)

    # If not requested to leave inactive instances in, remove them
    if not filter_spec.include_inactive:
        if query_set.model is User:
            query_set = query_set.filter(is_active=True)
        elif isinstance(query_set, SoftDeleteQuerySet):
            query_set = query_set.active()

    return query_set
