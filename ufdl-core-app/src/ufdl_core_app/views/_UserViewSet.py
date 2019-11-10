from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from ..models import User
from ..serialisers import UserSerialiser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerialiser

    permission_classes = [IsAdminUser]
