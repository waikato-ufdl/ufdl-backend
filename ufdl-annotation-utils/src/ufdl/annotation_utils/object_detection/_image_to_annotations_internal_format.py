from typing import Optional

from ufdl.json.object_detection import Image as JSONImage

from wai.annotations.domain.image import Image, ImageFormat
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance

from wai.common.adams.imaging.locateobjects import LocatedObjects

from wai.json.object import Absent

from ._located_object_from_annotation import located_object_from_annotation


def image_to_annotations_internal_format(
        image: Optional[JSONImage],
        filename: str,
        data: bytes
) -> ImageObjectDetectionInstance:
    """
    Converts an image record to the format expected by wai.annotations.

    :param image:       The image record.
    :param filename:    The image filename to use.
    :param data:        The image data to use.
    :return:            The wai.annotations internal-format record.
    """
    # Get the size of the image from the record
    size = None if image is None or image.dimensions is Absent else (image.width, image.height)

    # Create an image-info object from the image, or from the data if it is missing
    image_info = (
        Image.from_file_data(filename, data)
        if image is None else
        Image(filename, data, ImageFormat.for_extension(image.format), size)
    )

    # Create a located-objects list from the image's annotations, or an empty one if it is missing
    located_objects = (
        LocatedObjects()
        if image is None else
        LocatedObjects(map(located_object_from_annotation, image.annotations))
    )

    return ImageObjectDetectionInstance(image_info, located_objects)
