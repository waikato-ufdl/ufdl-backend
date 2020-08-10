from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

from ..apps import UFDLCoreAppConfig


class UserManager(DjangoUserManager):
    """
    Custom manager for working with groups of users.
    """
    def delete(self):
        # Don't delete users, just set their is_active flags to false
        num_deleted = self.update(is_active=False)

        return num_deleted, {self.model._meta.label: num_deleted}


class User(AbstractUser):
    """
    The base user model for all users of the UFDL system. Although this is currently
    identical to the Django User class, it is considered best practice to define
    your own user model, so it can be modified in future should the need arise.
    """
    # The node the user corresponds to (null for non-node users)
    node = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Node",
                             on_delete=models.DO_NOTHING,
                             related_name="user",
                             null=True,
                             default=None)

    @property
    def is_node(self) -> bool:
        """
        Whether the user is a worker node.
        """
        return self.node is not None

    objects = UserManager()

    def delete(self, using=None, keep_parents=False):
        # Don't delete users, just set their is_active flags to false
        self.is_active = False
        self.save()

        return 1, {User._meta.label: 1}
