from ..models import Project
from ._OrganisationInferableSerialiser import OrganisationInferableSerialiser
from ._UFDLBaseSerialiser import UFDLBaseSerialiser


class ProjectSerialiser(OrganisationInferableSerialiser, UFDLBaseSerialiser):
    class Meta:
        model = Project
        fields = ["id",
                  "name",
                  "organisation"] + UFDLBaseSerialiser.base_fields

    @classmethod
    def get_organisation_from_validated_data(cls, validated_data):
        return validated_data["organisation"]
