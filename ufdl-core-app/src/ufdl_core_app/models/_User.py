from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    The base user model for all users of the UFDL system. Although this is currently
    identical to the Django User class, it is considered best practice to define
    your own user model, so it can be modified in future should the need arise.
    """
    def active_membership_to(self, organisation):
        """
        Gets this user's membership to the given organisation,
        if they have one currently.

        :param organisation:    The organisation to get the membership to.
        :return:                The membership.
        """
        # Local imports to avoid circularity errors
        from ._Organisation import Organisation
        from ._Membership import Membership

        # Make sure the argument is an organisation
        if not isinstance(organisation, Organisation):
            raise TypeError(f"Expected {Organisation.__name__} but got {organisation.__class__.__name__} instead")

        # Get the active memberships between this user and the organisation
        # (should be zero or one)
        memberships = Membership.objects.active().filter(user=self, organisation=organisation)

        # Check the previous condition (very bad if it fails)
        num_memberships: int = len(memberships)
        if num_memberships > 1:
            raise AssertionError(f"Each user should have at most one active membership with "
                                 f"an organisation, but \"{self.username}\" has {num_memberships} "
                                 f"with \"{organisation.name}\"")

        # If no active memberships, return None
        if num_memberships == 0:
            return None

        # Otherwise there is one and only one, so return it
        return memberships[0]
