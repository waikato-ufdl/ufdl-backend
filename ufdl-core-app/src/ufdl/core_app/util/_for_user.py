from django.db import models
from simple_django_teams.models import Team, Membership


def for_user(query_set, user):
    """
    Filters a query-set for the given user.

    :param query_set:   The query-set to filter.
    :param user:        The user to filter the results for.
    :return:            The filtered results.
    """
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

    # Per-model filtering
    from ..models import Dataset, Project
    if query_set.model is Dataset:
        return query_set.filter(
            models.Q(Dataset.public_Q) |
            models.Q(project__team__in=for_user(Team.objects, user))
        )

    elif query_set.model is Project:
        return query_set.filter(
            team__in=for_user(Team.objects, user)
        )

    elif query_set.model is Membership:
        return query_set.filter(
            models.Q(user=user) |
            models.Q(team__in=Team.objects.user_is_admin_for(user))
        )

    elif query_set.model is Team:
        return query_set.filter(
            memberships__user=user,
            memberships__deletion_time__isnull=True)
