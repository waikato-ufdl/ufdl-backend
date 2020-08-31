from ..models import Project
from ..serialisers import ProjectSerialiser
from ..permissions import IsMember, MemberHasWritePermission, IsAuthenticated, AllowNone
from .mixins import SoftDeleteViewSet
from ._UFDLBaseViewSet import UFDLBaseViewSet


class ProjectViewSet(SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": MemberHasWritePermission,
        "retrieve": IsMember,
        "update": MemberHasWritePermission,
        "partial_update": MemberHasWritePermission,
        "destroy": MemberHasWritePermission,
        "hard_delete": AllowNone,
        "reinstate": AllowNone
    }
