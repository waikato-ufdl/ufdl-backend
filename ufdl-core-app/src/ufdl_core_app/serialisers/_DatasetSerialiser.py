from ..models import Dataset
from ._OrganisationInferableSerialiser import OrganisationInferableSerialiser


class DatasetSerialiser(OrganisationInferableSerialiser):
    class Meta:
        model = Dataset
        fields = ["name",
                  "version",
                  "creation_time",
                  "creator",
                  "deletion_time",
                  "project",
                  "licence",
                  "is_public",
                  "tags"]
        extra_kwargs = {
            "tags": {"allow_blank": True}
        }

    def create(self, validated_data):
        validated_data["creator"] = self.active_membership_for(self.context["request"].user)
        return super().create(validated_data)

    @classmethod
    def get_organisation_from_validated_data(cls, validated_data):
        return validated_data["project"].organisation
