class OrganisationInferable:
    """
    Interface for classes which can provide the organisation
    to which they belong (either directly or indirectly). Cannot
    be an ABC as this is used as a mixin on models, which use
    a different metaclass.
    """
    def infer_organisation(self):
        """
        Gets the inferred organisation for this object.

        :return:    The organisation.
        """
        raise NotImplementedError(OrganisationInferable.infer_organisation.__qualname__)

    def active_membership_for(self, user):
        """
        Gets the active membership for the given user, relative to
        this object's organisation.

        :param user:    The user.
        :return:        The membership, or None if none available.
        """
        return user.active_membership_to(self.infer_organisation())
