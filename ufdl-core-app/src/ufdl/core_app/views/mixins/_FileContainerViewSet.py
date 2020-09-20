from typing import List

from rest_framework import routers
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.json.core import FileMetadata

from ...exceptions import JSONParseFailure
from ...renderers import BinaryFileRenderer
from ...models.mixins import FileContainerModel
from ...serialisers import NamedFileSerialiser
from ._RoutedViewSet import RoutedViewSet


class FileContainerViewSet(RoutedViewSet):
    """
    Mixin for view-sets which can upload/download/delete contained files.
    """
    # The keyword used to specify when the view-set is in file-container mode
    FILE_MODE_KEYWORD: str = "file-container"

    # The keyword used to specify when the view-set is in file-container mode
    METADATA_MODE_KEYWORD: str = "file-metadata"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/files/(?P<fn>.*)$',
                mapping={'post': 'add_file',
                         'get': 'get_file',
                         'delete': 'delete_file'},
                name='{basename}-file-container',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: FileContainerViewSet.FILE_MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/metadata/(?P<fn>.+)$',
                mapping={'post': 'set_metadata',
                         'get': 'get_metadata'},
                name='{basename}-file-metadata',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: FileContainerViewSet.METADATA_MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/metadata{trailing_slash}$',
                mapping={'get': 'get_all_metadata'},
                name='{basename}-file-metadata',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: FileContainerViewSet.METADATA_MODE_KEYWORD}
            )
        ]

    def get_parsers(self):
        # If not posting a file, return the standard parsers
        if self.mode != FileContainerViewSet.FILE_MODE_KEYWORD or self.request.method != 'POST':
            return super().get_parsers()

        return [FileUploadParser()]

    def get_renderers(self):
        # If not getting a file, return the standard renderers
        if self.mode != FileContainerViewSet.FILE_MODE_KEYWORD or self.request.method != 'GET':
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
        container = self.get_object_of_type(FileContainerModel)

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
        container = self.get_object_of_type(FileContainerModel)

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
        container = self.get_object_of_type(FileContainerModel)

        # Delete the file
        record = container.delete_file(fn)

        return Response(NamedFileSerialiser().to_representation(record))

    def set_metadata(self, request: Request, pk=None, fn=None):
        """
        Action to set the meta-data of a file.

        :param request:     The request containing the file meta-data.
        :param pk:          The primary key of the file-container being accessed.
        :param fn:          The filename of the file being modified.
        :return:            A response containing the set meta-data.
        """
        # Get the container object
        container = self.get_object_of_type(FileContainerModel)

        # Get the meta-data from the request
        metadata = JSONParseFailure.attempt(dict(request.data), FileMetadata)

        # Set the metadata of the file
        container.set_file_metadata(fn, metadata.metadata)

        return Response(metadata.to_raw_json())

    def get_metadata(self, request: Request, pk=None, fn=None):
        """
        Action to retrieve the meta-data of a file.

        :param request:     The request.
        :param pk:          The primary key of the file-container being accessed.
        :param fn:          The filename of the file being accessed.
        :return:            A response containing the file's meta-data.
        """
        # Get the container object
        container = self.get_object_of_type(FileContainerModel)

        # Get the meta-data from the container
        metadata = container.get_file_metadata(fn)

        return Response(FileMetadata(metadata=metadata).to_raw_json())

    def get_all_metadata(self, request: Request, pk=None):
        """
        Action to retrieve the meta-data for all files in the container.

        :param request:     The request.
        :param pk:          The primary key of the file-container being accessed.
        :return:            A response containing the files' meta-data.
        """
        # Get the container object
        container = self.get_object_of_type(FileContainerModel)

        return Response(
            {fn: container.get_file_metadata(fn)
             for fn in container.iterate_filenames()}
        )
