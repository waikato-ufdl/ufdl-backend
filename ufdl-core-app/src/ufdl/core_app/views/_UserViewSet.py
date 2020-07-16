from ..models import User
from ..serialisers import UserSerialiser
from ._UFDLBaseViewSet import UFDLBaseViewSet


class UserViewSet(UFDLBaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerialiser

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