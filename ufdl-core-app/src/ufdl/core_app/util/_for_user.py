from django.db import models
from simple_django_teams.models import Team, Membership


def for_user(query_set, user):
    """
    Filters a query-set for the given user.

    :param query_set:   The query-set to filter.
    :param user:        The user to filter the results for.
    :return:            The filtered results.
    """
    from ..models.mixins import UserRestrictedQuerySet

    # Non-users can only view public models
    if not user.is_authenticated or not user.is_active:
        from ..models.mixins import PublicQuerySet
        if isinstance(query_set, PublicQuerySet):
            return query_set.public()
        else:
            return query_set.none()

    # Superusers/staff can view all models
    if user.is_superuser or user.is_staff:
        return query_set.all()

    # Per-model filtering (teams and memberships must be done
    # separately as they aren't controlled by this code-base)
    if query_set.model is Membership:
        # Users have access to their own memberships and the memberships
        # of any teams the user is an admin for
        query_set = query_set.filter(
            models.Q(user=user) |
            models.Q(team__in=Team.objects.user_is_admin_for(user))
        )
    elif query_set.model is Team:
        # Users have access to any team to which they are
        # an active member
        query_set = query_set.filter(
            memberships__user=user,
            memberships__deletion_time__isnull=True
        )
    elif isinstance(query_set, UserRestrictedQuerySet):
        query_set = query_set.for_user(user)

    return query_set
