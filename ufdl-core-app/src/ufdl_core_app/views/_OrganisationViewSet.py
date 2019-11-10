from rest_framework.permissions import IsAuthenticated

from ..models import Organisation
from ..serialisers import OrganisationSerialiser
from ._PerActionPermissionsModelViewSet import PerActionPermissionsModelViewSet


class OrganisationViewSet(PerActionPermissionsModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerialiser

    default_permissions = []

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }

