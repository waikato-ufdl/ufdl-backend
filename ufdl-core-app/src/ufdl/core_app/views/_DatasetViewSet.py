from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import Dataset
from ..serialisers import DatasetSerialiser, DataAssetSerialiser
from ..permissions import MemberHasWritePermission, IsMember, IsPublic, IsAdminUser
from .mixins import AsFileViewSet
from ._UFDLBaseViewSet import UFDLBaseViewSet


class DatasetViewSet(AsFileViewSet, UFDLBaseViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerialiser

    admin_permission_class = IsAdminUser | MemberHasWritePermission

    permission_classes = {
        "list": [AllowAny],  # List filtering is done seperately
        "retrieve": [IsMember | IsPublic],
        "as_file": [AllowAny]
    }

    @action(detail=True, methods=["post"],
            url_path="add-file",
            url_name="add-file",
            permission_classes=[AllowAny],  # TODO: Change to a proper level of authorisation
            parser_classes=[FileUploadParser])
    def add_file(self, request: Request, pk=None):
        """
        Action to add a file to a dataset.

        :param request:     The request containing the file data.
        :return:            The response containing the disk-file record.
        """
        # Get the file from the request
        file = request.data['file']

        # Create the disk-file record from the data
        asset = self.get_object().add_file(file.name, file.file.read())

        return Response(DataAssetSerialiser().to_representation(asset))

    @action(detail=True, methods=["post"],
            url_path="delete-file",
            url_name="delete-file",
            permission_classes=[AllowAny]  # TODO: Change to a proper level of authorisation
            )
    def delete_file(self, request: Request, pk=None):
        """
        Action to add a file to a dataset.

        :param request:     The request containing the file data.
        :return:            The response containing the disk-file record.
        """
        # Get the name of the file to delete
        filename = request.data["filename"]

        # Delete the file
        asset = self.get_object().delete_file(filename)

        return Response(DataAssetSerialiser().to_representation(asset))

    @action(detail=True, methods=["post"],
            url_path="copy",
            url_name="copy",
            permission_classes=[AllowAny]  # TODO: Change to a proper level of authorisation
            )
    def copy(self, request: Request, pk=None):
        """
        Action to copy a dataset.

        :param request:     The request containing the file data.
        :return:            The response containing the new dataset record.
        """
        # Get the new name for the copy if one was provided
        new_name = request.data["new_name"] if "new_name" in request.data else None

        # Copy the dataset
        dataset = self.get_object().copy(request.user, new_name)

        return Response(DatasetSerialiser().to_representation(dataset))
