from ..models import Membership
from ._OrganisationInferableSerialiser import OrganisationInferableSerialiser
from ._UFDLBaseSerialiser import UFDLBaseSerialiser


class MembershipSerialiser(OrganisationInferableSerialiser, UFDLBaseSerialiser):
    class Meta:
        model = Membership
        fields = ["user",
                  "organisation",
                  "permissions"] + UFDLBaseSerialiser.base_fields

    @classmethod
    def get_organisation_from_validated_data(cls, validated_data):
        return validated_data["organisation"]
