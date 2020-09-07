"""
Because GET requests can't have bodies, and we need one to filter the results of the list
action, the standard CRUD routes are redefined here to support this.

Original definitions: rest_framework/routers.py
"""
from rest_framework.routers import Route

# The standard CRUD routes
STANDARD_CRUD_ROUTES = [
    # List route.
    Route(
        url=r'^{prefix}/list{trailing_slash}$',
        mapping={
            'post': 'list'
        },
        name='{basename}-list',
        detail=False,
        initkwargs={'suffix': 'List'}
    ),
    # Create route.
    Route(
        url=r'^{prefix}/create{trailing_slash}$',
        mapping={
            'post': 'create'
        },
        name='{basename}-create',
        detail=False,
        initkwargs={'suffix': 'List'}
    ),
    # Detail route.
    Route(
        url=r'^{prefix}/{lookup}{trailing_slash}$',
        mapping={
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        },
        name='{basename}-detail',
        detail=True,
        initkwargs={'suffix': 'Instance'}
    )
]
