from django.db import models

from ..apps import APP_NAME
from ._OrganisationInferable import OrganisationInferable
from ._UFDLBaseModel import UFDLBaseModel, UFDLBaseQuerySet


class OrganisationQuerySet(UFDLBaseQuerySet):
    """
    Custom query-set for organisations.
    """
    def pre_delete(self):
        # Local import to avoid circular references
        from ._Project import Project
        from ._Membership import Membership

        # Delete any active projects
        Project.objects.filter(organisation__in=self).delete()

        # Delete any active memberships
        Membership.objects.filter(organisation__in=self).delete()

    def for_user(self, user):
        """
        Filters the queryset to those organisations the user can see.

        :param user:    The user.
        :return:        The organisations.
        """
        # Unauthenticated/inactive users can't see anything
        if not user.is_authenticated or not user.is_active:
            return self.none()

        # Superusers/staff can see all organisations
        if user.is_superuser or user.is_staff:
            return self.all()

        return self.filter(memberships__user=user,
                           memberships__deletion_time__isnull=True)

    def user_is_admin_for(self, user):
        """
        Filters the organisations to those the given user is an
        admin for.

        :param user:    The user.
        :return:        The organisations.
        """
        # Local import to avoid circular references
        from ._Membership import Membership

        # Unauthenticated users can't be admins
        if not user.is_authenticated:
            return self.none()

        # Superusers/staff are honourary admins for all organisations
        if user.is_superuser or user.is_staff:
            return self.all()

        return self.filter(memberships__permissions=Membership.PERMISSION_ADMIN,
                           memberships__deletion_time__isnull=True,
                           memberships__user=user)


class Organisation(OrganisationInferable, UFDLBaseModel):
    """
    An organisation represents a collection of users and the projects
    that they are working on.
    """
    # The name of the organisation
    name = models.CharField(max_length=200)

    # The members of the organisation
    members = models.ManyToManyField(f"{APP_NAME}.User",
                                     through=f"{APP_NAME}.Membership",
                                     through_fields=("organisation", "user"),
                                     related_name="organisations")

    objects = OrganisationQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each active organisation has a unique name
            models.UniqueConstraint(name="unique_active_organisation_names",
                                    fields=["name"],
                                    condition=UFDLBaseModel.active_Q)
        ]

    def infer_organisation(self) -> "Organisation":
        return self

    def pre_delete(self):
        # Delete any active projects
        self.projects.all().delete()

        # Delete any active memberships
        self.memberships.all().delete()

    def __str__(self) -> str:
        return self.name
