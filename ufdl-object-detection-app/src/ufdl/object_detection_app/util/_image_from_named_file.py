from ufdl.core_app.models.files import NamedFile

from ufdl.json.object_detection import Image

from wai.annotations.core import ImageInfo


def image_from_named_file(file: NamedFile) -> Image:
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
