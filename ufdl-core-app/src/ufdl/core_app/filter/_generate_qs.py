from typing import List

from django.db.models import Q

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import *
from ufdl.json.core.filter.logical import *


def generate_qs(expressions: List[FilterExpression]) -> List[Q]:
    """
    Generates the Q filters based on the provided expressions.

    :param expressions:     The filter expressions to generate Qs from.
    :return:                A list of Q objects.
    """
    return [generate_q_from_expression(expression)
            for expression in expressions]


def generate_q_from_expression(expression: FilterExpression) -> Q:
    """
    Generates a Q object from the given expression description.

    :param expression:  The expression.
    :return:            The Q filter object.
    """
    if isinstance(expression, Contains):
        return generate_q_from_contains(expression)
    elif isinstance(expression, Exact):
        return generate_q_from_exact(expression)
    elif isinstance(expression, IsNull):
        return generate_q_from_isnull(expression)
    elif isinstance(expression, Compare):
        return generate_q_from_compare(expression)
    elif isinstance(expression, And):
        return generate_q_from_and(expression)
    elif isinstance(expression, Or):
        return generate_q_from_or(expression)
    else:
        raise Exception(f"Unsupported filter expression type: {expression.__class__.__name__}")


def generate_q_from_compare(expression: Compare) -> Q:
    """
    Generates a Q object from a 'compare' expression.

    :param expression:  The 'compare' expression.
    :return:            The Q filter object.
    """
    # Generate the keyword expected by the Q constructor
    keyword = expression.field + ("__lt" if expression.operator == "<"
                                  else "__gt" if expression.operator == ">"
                                  else "__lte" if expression.operator == "<="
                                  else "__gte")

    # Create the Q object
    q = Q(**{keyword: expression.value})

    # Handle negation and return
    return handle_negation(expression, q)


def generate_q_from_contains(expression: Contains) -> Q:
    """
    Generates a Q object from a 'contains' expression.

    :param expression:  The 'contains' expression.
    :return:            The Q filter object.
    """
    # Generate the keyword expected by the Q constructor
    keyword = expression.field + ("__icontains" if expression.case_insensitive else "__contains")

    # Create the Q object
    q = Q(**{keyword: expression.sub_string})

    # Handle negation and return
    return handle_negation(expression, q)


def generate_q_from_exact(expression: Exact) -> Q:
    """
    Generates a Q object from an 'exact' expression.

    :param expression:  The 'exact' expression.
    :return:            The Q filter object.
    """
    # Generate the keyword expected by the Q constructor
    keyword = expression.field + ("__iexact" if expression.case_insensitive else "__exact")

    # Create the Q object
    q = Q(**{keyword: expression.value})

    # Handle negation and return
    return handle_negation(expression, q)


def generate_q_from_isnull(expression: IsNull) -> Q:
    """
    Generates a Q object from an 'isnull' expression.

    :param expression:  The 'isnull' expression.
    :return:            The Q filter object.
    """
    # Generate the keyword expected by the Q constructor
    keyword = expression.field + "__isnull"

    # Create the Q object
    q = Q(**{keyword: True})

    # Handle negation and return
    return handle_negation(expression, q)


def generate_q_from_and(expression: And) -> Q:
    """
    Generates a Q object from an 'and' expression.

    :param expression:  The 'and' expression.
    :return:            The Q filter object.
    """
    # Generate a Q object for each sub-expression
    sub_qs = generate_qs(expression.sub_expressions)

    # Combine them using the and operator
    q = sub_qs[0]
    for sub_q in sub_qs[1:]:
        q = q & sub_q

    # Handle negation and return
    return handle_negation(expression, q)


def generate_q_from_or(expression: Or) -> Q:
    """
    Generates a Q object from an 'or' expression.

    :param expression:  The 'or' expression.
    :return:            The Q filter object.
    """
    # Generate a Q object for each sub-expression
    sub_qs = generate_qs(expression.sub_expressions)

    # Combine them using the or operator
    q = sub_qs[0]
    for sub_q in sub_qs[1:]:
        q = q | sub_q

    # Handle negation and return
    return handle_negation(expression, q)


def handle_negation(expression: FilterExpression, q: Q) -> Q:
    """
    Handles the negation flag in the expression.

    :param expression:      The filtering expression.
    :param q:               The Q object, disregarding negation.
    :return:                The Q object, with negation applied.
    """
    if expression.invert:
        return ~q
    else:
        return q
