from ..models import LogEntry
from ..serialisers import LogEntrySerialiser
from ..permissions import IsAuthenticated, AllowNone
from ._UFDLBaseViewSet import UFDLBaseViewSet


class LogEntryViewSet(UFDLBaseViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": IsAuthenticated,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone
    }
