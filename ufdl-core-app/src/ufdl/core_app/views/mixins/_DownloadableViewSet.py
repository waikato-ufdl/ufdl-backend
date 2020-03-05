from typing import List

from rest_framework import routers
from rest_framework.exceptions import UnsupportedMediaType
from rest_framework.request import Request
from rest_framework.response import Response

from ...models.mixins import AsFileModel
from ...renderers import BinaryFileRenderer
from ...util import format_query_params
from ._RoutedViewSet import RoutedViewSet

# The name of the parameter specifying the file-format
FILE_FORMAT_PARAMETER: str = "filetype"


class DownloadableViewSet(RoutedViewSet):
    """
    Mixin for view-sets which can provide their objects
    as files for download.
    """
    # The keyword used to specify when the view-set is in downloadable mode
    MODE_KEYWORD: str = "downloadable"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/download{trailing_slash}$',
                mapping={'get': 'download'},
                name='{basename}-download',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: DownloadableViewSet.MODE_KEYWORD}
            )
        ]

    def get_renderers(self):
        # If not getting a file, return the standard renderers
        if self.mode != DownloadableViewSet.MODE_KEYWORD:
            return super().get_renderers()

        return [BinaryFileRenderer()]

    def download(self, request: Request, pk=None):
        """
        Gets the instance as a file in a particular format.

        :param request:     The request.
        :return:            The response containing the file data.
        """
        # Get the instance
        obj = self.get_object()

        # The object must be able to be converted to a file
        if not isinstance(obj, AsFileModel):
            raise TypeError(f"Object-type '{type(obj).__name__}' cannot be exported as a file")

        # Get the parameters
        parameters = format_query_params(request)

        # Get the format to send the file as
        file_format = parameters.pop(FILE_FORMAT_PARAMETER, obj.default_format())

        # Must specify exactly one format
        if isinstance(file_format, list):
            raise ValueError(f"Multiple file formats specified")

        # The object must support the file format
        if not obj.supports_file_format(file_format):
            raise UnsupportedMediaType(file_format)

        # Create a filename for the file
        filename: str = f"{obj.filename_without_extension()}.{file_format}"

        return Response(data=obj.as_file(file_format, **parameters),
                        content_type=BinaryFileRenderer.media_type,
                        headers={"Content-Disposition": f"attachment; filename={filename}"})
