from ...models.jobs import JobType
from ...serialisers.jobs import JobTypeSerialiser
from ...permissions import IsAuthenticated, AllowNone
from .._UFDLBaseViewSet import UFDLBaseViewSet
from ..mixins import GetAllValuesOfTypeViewSet


class JobTypeViewSet(GetAllValuesOfTypeViewSet, UFDLBaseViewSet):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone,
        "get_all_values_of_type": IsAuthenticated
    }
