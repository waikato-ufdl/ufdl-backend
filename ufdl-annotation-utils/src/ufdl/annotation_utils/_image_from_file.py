from ufdl.json.object_detection import Image

from wai.annotations.core import ImageInfo


def image_from_file(filename: str, file_data: bytes) -> Image:
    """
    Creates an empty Image object for the given file.

    :param filename:    The filename of the file.
    :param file_data:   The file's data.
    :return:            The Image object.
    """
    # Create an image-info record from the file
    image_info = ImageInfo(filename, file_data)

    return Image(format=image_info.format.get_default_extension(),
                 dimensions=[image_info.width(), image_info.height()],
                 annotations=[])
