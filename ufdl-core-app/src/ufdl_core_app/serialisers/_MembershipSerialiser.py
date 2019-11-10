from ..models import Membership
from ._OrganisationInferableSerialiser import OrganisationInferableSerialiser


class MembershipSerialiser(OrganisationInferableSerialiser):
    class Meta:
        model = Membership
        fields = ["user",
                  "organisation",
                  "joined_time",
                  "deletion_time",
                  "permissions"]

    @classmethod
    def get_organisation_from_validated_data(cls, validated_data):
        return validated_data["organisation"]
