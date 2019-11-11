from ..models import Dataset
from ._OrganisationInferableSerialiser import OrganisationInferableSerialiser
from ._UFDLBaseSerialiser import UFDLBaseSerialiser


class DatasetSerialiser(OrganisationInferableSerialiser, UFDLBaseSerialiser):
    class Meta:
        model = Dataset
        fields = ["name",
                  "version",
                  "project",
                  "licence",
                  "is_public",
                  "tags"] + UFDLBaseSerialiser.base_fields
        extra_kwargs = {
            "tags": {"allow_blank": True}
        }

    @classmethod
    def get_organisation_from_validated_data(cls, validated_data):
        return validated_data["project"].organisation
