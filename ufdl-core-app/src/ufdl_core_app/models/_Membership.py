from django.db import models

from ..apps import APP_NAME
from ._OrganisationInferable import OrganisationInferable
from ._SoftDeleteModel import SoftDeleteModel, SoftDeleteQuerySet


class MembershipQuerySet(SoftDeleteQuerySet):
    """
    Custom query-set for memberships.
    """
    def for_user(self, user):
        """
        Filters the queryset to those entries which the given
        user is allowed to see.

        :param user:    The user.
        :return:        The memberships.
        """
        # Local import to avoid circular reference
        from ._Organisation import Organisation

        # Non-users can't view memberships
        if not user.is_authenticated or not user.is_active:
            return self.none()

        # Superusers/staff can view all memberships
        if user.is_superuser or user.is_staff:
            return self.all()

        return self.filter(models.Q(user=user) |
                           models.Q(organisation__in=Organisation.objects.user_is_admin_for(user)))

    def admins(self):
        """
        Returns those memberships that are admins.

        :return:    The memberships.
        """
        return self.filter(permissions=Membership.PERMISSION_ADMIN)


class Membership(OrganisationInferable, SoftDeleteModel):
    # Permission constants
    PERMISSION_READ = "R"
    PERMISSION_WRITE = "W"
    PERMISSION_ADMIN = "A"

    # The user whose membership this is
    user = models.ForeignKey(f"{APP_NAME}.User",
                             on_delete=models.DO_NOTHING,
                             related_name="memberships")

    # The organisation to which this membership applies
    organisation = models.ForeignKey(f"{APP_NAME}.Organisation",
                                     on_delete=models.DO_NOTHING,
                                     related_name="memberships")

    # The date/time the member joined the organisation
    joined_time = models.DateTimeField(auto_now_add=True,
                                       editable=False)

    # The permissions the member has within the organisation
    permissions = models.CharField(max_length=1,
                                   choices=[
                                       (PERMISSION_READ, "Read"),
                                       (PERMISSION_WRITE, "Write"),
                                       (PERMISSION_ADMIN, "Admin")
                                   ],
                                   default=PERMISSION_READ)

    # The manager for this model
    objects = MembershipQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each user is only an active member of each organisation once
            models.UniqueConstraint(name="one_active_membership_per_user_per_organisation",
                                    fields=["user", "organisation"],
                                    condition=SoftDeleteModel.active_Q)
        ]

    def is_admin(self) -> bool:
        """
        Whether the member is an admin for this organisation.
        """
        return self.permissions == self.PERMISSION_ADMIN

    def infer_organisation(self):
        return self.organisation

    def __str__(self) -> str:
        return f"User \"{self.user}\" at organisation \"{self.organisation}\""
