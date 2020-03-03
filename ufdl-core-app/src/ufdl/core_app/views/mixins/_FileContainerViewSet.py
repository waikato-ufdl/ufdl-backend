from typing import List

from rest_framework import routers
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response

from ...renderers import BinaryFileRenderer
from ...models.mixins import FileContainerModel
from ...serialisers import NamedFileSerialiser
from ._RoutedViewSet import RoutedViewSet


class FileContainerViewSet(RoutedViewSet):
    """
    Mixin for view-sets which can upload/download/delete contained files.
    """
    # The keyword used to specify when the view-set is in file-container mode
    MODE_KEYWORD: str = "file-container"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/files/(?P<fn>.*)$',
                mapping={'post': 'add_file'},
                name='{basename}-file-container-new',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: FileContainerViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/files/(?P<fn>.+)$',
                mapping={'get': 'get_file',
                         'delete': 'delete_file'},
                name='{basename}-file-container-existing',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: FileContainerViewSet.MODE_KEYWORD}
            )
        ]

    def get_parsers(self):
        # If not posting a file, return the standard parsers
        if self.mode != FileContainerViewSet.MODE_KEYWORD or self.request.method != 'POST':
            return super().get_parsers()

        return [FileUploadParser()]

    def get_renderers(self):
        # If not getting a file, return the standard renderers
        if self.mode != FileContainerViewSet.MODE_KEYWORD or self.request.method != 'GET':
            return super().get_renderers()

        return [BinaryFileRenderer()]

    def add_file(self, request: Request, pk=None, fn=None):
        """
        Action to add a file to a object.

        :param request:     The request containing the file data.
        :param pk:          The primary key of the container object.
        :param fn:          The filename of the file being added.
        :return:            The response containing the file record.
        """
        # Get the container object
        container = self.get_object()

        # Must be a container model
        if not isinstance(container, FileContainerModel):
            raise TypeError(f"{type(container).__name__} is not a file-container model")

        # Create the file record from the data
        record = container.add_file(fn, request.data['file'].file.read())

        return Response(NamedFileSerialiser().to_representation(record))

    def get_file(self, request: Request, pk=None, fn=None):
        """
        Gets a file from the dataset for download.

        :param request:     The request.
        :param pk:          The primary key of the dataset being accessed.
        :param fn:          The filename of the file being asked for.
        :return:            The response containing the file.
        """
        # Get the container object
        container = self.get_object()

        # Must be a container model
        if not isinstance(container, FileContainerModel):
            raise TypeError(f"{type(container).__name__} is not a file-container model")

        return Response(container.get_file(fn))

    def delete_file(self, request: Request, pk=None, fn=None):
        """
        Action to add a file to a dataset.

        :param request:     The request containing the file data.
        :param pk:          The primary key of the dataset being accessed.
        :param fn:          The filename of the file being deleted.
        :return:            The response containing the disk-file record.
        """
        # Get the container object
        container = self.get_object()

        # Must be a container model
        if not isinstance(container, FileContainerModel):
            raise TypeError(f"{type(container).__name__} is not a file-container model")

        # Delete the file
        record = container.delete_file(fn)

        return Response(NamedFileSerialiser().to_representation(record))
