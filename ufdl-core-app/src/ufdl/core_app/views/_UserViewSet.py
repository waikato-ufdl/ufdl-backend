from ..models import User
from ..permissions import IsSelf, AllowNone
from ..serialisers import UserSerialiser
from .mixins import GetByNameViewSet
from ._UFDLBaseViewSet import UFDLBaseViewSet


class UserViewSet(GetByNameViewSet, UFDLBaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerialiser

    permission_classes = {
        "list": AllowNone,
        "create": AllowNone,
        "retrieve": IsSelf,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone,
        "get_by_name": IsSelf
    }

    def format_request_log_message(self, request) -> str:
        # Identical to UFDLBaseViewSet.format_request_log_message, but
        # redacts the password from the log
        data = dict(request.data)
        if "password" in data:
            data["password"] = "<REDACTED>"

        return (
            f"URI='{request.get_raw_uri()}'\n"
            f"METHOD='{request.method}'\n"
            f"ACTION='{self.action}'\n"
            f"DATA={data}\n"
            f"USER={request.user}\n"
        )
