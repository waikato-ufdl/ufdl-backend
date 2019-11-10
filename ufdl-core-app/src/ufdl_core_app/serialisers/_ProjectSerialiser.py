from ..models import Project
from ._OrganisationInferableSerialiser import OrganisationInferableSerialiser


class ProjectSerialiser(OrganisationInferableSerialiser):
    class Meta:
        model = Project
        fields = ["name",
                  "creation_time",
                  "deletion_time",
                  "organisation"]

    def create(self, validated_data):
        validated_data["creator"] = self.active_membership_for(self.context["request"].user)
        return super().create(validated_data)

    @classmethod
    def get_organisation_from_validated_data(cls, validated_data):
        return validated_data["organisation"]
