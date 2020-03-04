from typing import List, Optional, Union

from wai.annotations.core import ImageInfo, ImageFormat, InternalFormat as AnnotationsInternalFormat

from wai.common.adams.imaging.locateobjects import LocatedObjects

from wai.json.object import StrictJSONObject, Absent
from wai.json.object.property import ArrayProperty, StringProperty, NumberProperty

from ufdl.core_app.models.files import File, NamedFile

from ._Annotation import Annotation


class Image(StrictJSONObject['Image']):
    """
    Represents a single image and its annotations.
    """
    # The image's format
    format: str = StringProperty(optional=True)

    # The image's dimensions
    dimensions: List[int] = ArrayProperty(
        element_property=NumberProperty(integer_only=True, minimum=1),
        min_elements=2, max_elements=2,
        optional=True
    )

    # The annotations of the image
    annotations: List[Annotation] = ArrayProperty(
        element_property=Annotation.as_property()
    )

    @staticmethod
    def from_file(file: NamedFile) -> 'Image':
        """
        Creates an empty Image object for the given file.

        :param file:    The file to read.
        :return:        The Image object.
        """
        # Create an image-info record from the file
        image_info = ImageInfo(file.filename, file.get_data())

        return Image(format=image_info.format.get_default_extension(),
                     dimensions=[image_info.width(), image_info.height()],
                     annotations=[])

    def to_annotations_internal_format(self, filename: str, data: bytes) -> AnnotationsInternalFormat:
        """
        Converts this image record to the format expected by wai.annotations.

        :param filename:    The image filename to use.
        :param data:        The image data to use.
        :return:            The wai.annotations internal-format record.
        """
        size = None if self.dimensions is Absent else (self.width, self.height)

        return (
            ImageInfo(filename, data, ImageFormat.for_extension(self.format), size),
            LocatedObjects(map(Annotation.to_located_object, self.annotations))
        )

    @property
    def width(self) -> Optional[int]:
        """
        Gets the width from the dimensions.

        :return:    The width, or None if not available.
        """
        if self.dimensions is not Absent:
            return self.dimensions[0]

    @property
    def height(self) -> Optional[int]:
        """
        Gets the height from the dimensions.

        :return:    The height, or None if not available.
        """
        if self.dimensions is not Absent:
            return self.dimensions[1]
