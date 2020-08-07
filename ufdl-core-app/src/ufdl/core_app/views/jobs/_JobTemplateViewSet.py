from ...models.jobs import JobTemplate
from ...serialisers.jobs import JobTemplateSerialiser
from ...permissions import IsAuthenticated, IsAdminUser
from ..mixins import SoftDeleteViewSet, InputsParametersViewSet, CreateJobViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class JobTemplateViewSet(CreateJobViewSet, InputsParametersViewSet, SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = JobTemplate.objects.all()
    serializer_class = JobTemplateSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }
