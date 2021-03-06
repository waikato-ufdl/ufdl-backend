from ...models.jobs import JobTemplate
from ...serialisers.jobs import JobTemplateSerialiser
from ...permissions import IsAuthenticated, AllowNone, IsAdminUser
from ..mixins import SoftDeleteViewSet, CreateJobViewSet, ImportTemplateViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class JobTemplateViewSet(ImportTemplateViewSet,
                         CreateJobViewSet,
                         SoftDeleteViewSet,
                         UFDLBaseViewSet):
    queryset = JobTemplate.objects.all()
    serializer_class = JobTemplateSerialiser

    admin_permission_class = AllowNone

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": IsAdminUser,
        "create_job": IsAuthenticated,
        "hard_delete": IsAdminUser,
        "reinstate": IsAdminUser,
        "import_template": IsAdminUser,
        "export_template": IsAdminUser
    }
