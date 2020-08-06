from typing import List

from rest_framework import routers
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response

from ...models.mixins import SetFileModel
from ._RoutedViewSet import RoutedViewSet


class SetFileViewSet(RoutedViewSet):
    """
    Mixin for view-sets which can have a file set against themselves.
    """
    # The keyword used to specify when the view-set is in set-file mode
    MODE_KEYWORD: str = "set-file"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/data{trailing_slash}$',
                mapping={'post': 'set_file',
                         'delete': 'delete_file'},
                name='{basename}-set-file',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: SetFileViewSet.MODE_KEYWORD}
            )
        ]

    def get_parsers(self):
        # If not posting a file, return the standard parsers
        if self.mode != SetFileViewSet.MODE_KEYWORD or self.request.method != 'POST':
            return super().get_parsers()

        return [FileUploadParser()]

    def set_file(self, request: Request, pk=None):
        """
        Action to set the file-data of an object.

        :param request:     The request containing the file data.
        :param pk:          The primary key of the container object.
        :return:            The response containing the file record.
        """
        # Get the set-file object
        obj = self.get_object_of_type(SetFileModel)

        # Set the file to the supplied data
        obj.set_file(request.data['file'].file.read())

        return Response(self.get_serializer().to_representation(obj))

    def delete_file(self, request: Request, pk=None):
        """
        Action to delete the file-data of an object.

        :param request:     The request.
        :param pk:          The primary key of the container object.
        :return:            The response containing the file record.
        """
        # Get the set-file object
        obj = self.get_object_of_type(SetFileModel)

        # Set the file to nothing
        obj.set_file(None)

        return Response(self.get_serializer().to_representation(obj))
