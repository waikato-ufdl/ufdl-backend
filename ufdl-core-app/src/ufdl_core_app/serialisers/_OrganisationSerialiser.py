from ..models import Organisation
from ._UFDLBaseSerialiser import UFDLBaseSerialiser


class OrganisationSerialiser(UFDLBaseSerialiser):
    class Meta:
        model = Organisation
        fields = ["name"] + UFDLBaseSerialiser.base_fields
