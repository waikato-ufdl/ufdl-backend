from ufdl.json.object_detection import Image

from wai.annotations.domain.image import ImageInfo, ImageFormat
from wai.annotations.domain.image.object_detection import ObjectDetectionInstance

from wai.common.adams.imaging.locateobjects import LocatedObjects

from wai.json.object import Absent

from ._located_object_from_annotation import located_object_from_annotation


def image_to_annotations_internal_format(image: Image, filename: str, data: bytes) -> ObjectDetectionInstance:
    """
    Converts an image record to the format expected by wai.annotations.

    :param image:       The image record.
    :param filename:    The image filename to use.
    :param data:        The image data to use.
    :return:            The wai.annotations internal-format record.
    """
    # Get the size of the image from the record
    size = None if image.dimensions is Absent else (image.width, image.height)

    return ObjectDetectionInstance(
        ImageInfo(filename, data, ImageFormat.for_extension(image.format), size),
        LocatedObjects(map(located_object_from_annotation, image.annotations))
    )
