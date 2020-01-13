from ..models import Project
from ..serialisers import ProjectSerialiser
from ..permissions import IsMember, MemberHasWritePermission, IsAdminUser, IsAuthenticated
from ._UFDLBaseViewSet import UFDLBaseViewSet


class ProjectViewSet(UFDLBaseViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerialiser

    admin_permission_class = IsAdminUser | MemberHasWritePermission
    default_permissions = []

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsMember]
    }
