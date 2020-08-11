from django.db import models


class UserRestrictedQuerySet(models.QuerySet):
    """
    Query-set base class for models which apply per-instance permissions
    based on the user accessing them.
    """
    def for_user(self, user):
        """
        Filters the query-set to those instances that the
        given user is allowed to access.

        :param user:    The user.
        :return:        The filtered query-set.
        """
        raise NotImplementedError(UserRestrictedQuerySet.for_user.__qualname__)
