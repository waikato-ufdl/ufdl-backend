from rest_framework import serializers


class OrganisationInferableSerialiser(serializers.ModelSerializer):
    """
    Mixin class for serialisers that can extract an organisation
    from their data payload.
    """
    def infer_organisation(self):
        """
        Gets the inferred organisation from this serialiser's payload.

        :return:    The organisation.
        """
        # Make sure we're valid
        self.is_valid(raise_exception=True)

        # Get the organisation from the validated data
        return self.get_organisation_from_validated_data(self.validated_data)

    @classmethod
    def get_organisation_from_validated_data(cls, validated_data):
        """
        Gets the organisation from the validated data of the serialiser.

        :param validated_data:  The validated data.
        :return:                The organisation.
        """
        raise NotImplementedError(OrganisationInferableSerialiser.get_organisation_from_validated_data.__qualname__)

    def active_membership_for(self, user):
        """
        Gets the active membership for the given user, relative to
        this object's organisation.

        :param user:    The user.
        :return:        The membership, or None if none available.
        """
        return user.active_membership_to(self.infer_organisation())
