from ...models.jobs import JobTemplate
from ...serialisers.jobs import JobTemplateSerialiser
from ...permissions import IsAuthenticated, AllowNone
from ..mixins import SoftDeleteViewSet, InputsParametersViewSet, CreateJobViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class JobTemplateViewSet(CreateJobViewSet, InputsParametersViewSet, SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = JobTemplate.objects.all()
    serializer_class = JobTemplateSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone,
        "create_job": IsAuthenticated,
        "add_input": AllowNone,
        "delete_input": AllowNone,
        "add_parameter": AllowNone,
        "delete_parameter": AllowNone,
        "hard_delete": AllowNone,
        "reinstate": AllowNone
    }
