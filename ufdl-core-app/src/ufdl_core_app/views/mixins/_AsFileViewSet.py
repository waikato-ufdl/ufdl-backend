from rest_framework import viewsets
from rest_framework.exceptions import UnsupportedMediaType
from rest_framework.request import Request
from rest_framework.response import Response

from ...models.mixins import AsFileModel
from ...renderers import BinaryFileRenderer

# The keyword argument name
KWARG: str = "as_file"

# The name of the parameter specifying the file-format
FILE_FORMAT_PARAMETER: str = "filetype"


class AsFileViewSet(viewsets.ModelViewSet):
    """
    Mixin for view-sets which can provide their objects
    as files.
    """
    # The file format that was requested
    as_file_called: bool = property(lambda self: self._as_file_called)

    def __init__(self, **kwargs):
        # Extract the format to save as
        self._as_file_called = kwargs.pop(KWARG, False)

        super().__init__(**kwargs)

    def get_renderers(self):
        # If not calling as_file, return the standard renderers
        if not self.as_file_called:
            return super().get_renderers()

        return [BinaryFileRenderer()]

    def as_file(self, request: Request, pk=None):
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
        parameters = dict(**request.query_params)

        # Get the format to send the file as
        file_format = parameters.pop(FILE_FORMAT_PARAMETER, [obj.default_format()])

        # Must specify exactly one format
        if len(file_format) > 1:
            raise ValueError(f"Multiple file formats specified")
        file_format = file_format[0]

        # The object must support the file format
        if not obj.supports_file_format(file_format):
            raise UnsupportedMediaType(file_format)

        # Create a filename for the file
        filename: str = f"{obj.filename_without_extension()}.{file_format}"

        return Response(data=obj.as_file(file_format, **parameters),
                        content_type=BinaryFileRenderer.media_type,
                        headers={"Content-Disposition": f"attachment; filename={filename}"})
