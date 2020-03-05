from rest_framework.request import Request

from ._typing import QueryParameters


def format_query_params(request: Request) -> QueryParameters:
    """
    Formats the query parameters from a GET request.

    :param request:     The GET request.
    :return:            A dictionary from parameter to:
                        - The single value if the parameter was specified once.
                        - The list of values supplied if the parameter was
                          specified more than once.
    """
    # Get the query parameters from the request
    # (all values will be lists)
    params = dict(**request.query_params)

    # Unpack any lists of length one into single values
    return {key: value if len(value) != 1 else value[0]
            for key, value in params.items()}
