from rest_framework.permissions import IsAdminUser

from ..models import Project
from ..serialisers import ProjectSerialiser
from ..permissions import IsMember, MemberHasWritePermission
from ._PerActionPermissionsModelViewSet import PerActionPermissionsModelViewSet


class ProjectViewSet(PerActionPermissionsModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerialiser

    admin_permission_class = IsAdminUser | MemberHasWritePermission
    default_permissions = []

    permission_classes = {
        "list": [IsMember],  # List filtering is done seperately
        "retrieve": [IsMember]
    }
