from rest_framework.permissions import AllowAny

from ..models import LogEntry
from ..serialisers import LogEntrySerialiser
from ..permissions import IsAuthenticated, IsAdminUser
from ._UFDLBaseViewSet import UFDLBaseViewSet


class LogEntryViewSet(UFDLBaseViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [AllowAny],  # List filtering is done seperately
        "create": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }
