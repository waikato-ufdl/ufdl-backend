from ufdl.json.object_detection import Image as JSONImage

from wai.annotations.domain.image import Image


def image_from_file(filename: str, file_data: bytes) -> JSONImage:
    """
    Creates an empty Image object for the given file.

    :param filename:    The filename of the file.
    :param file_data:   The file's data.
    :return:            The Image object.
    """
    # Create an image-info record from the file
    image_info = Image.from_file_data(filename, file_data)

    return JSONImage(
        format=image_info.format.get_default_extension(),
        dimensions=[image_info.width, image_info.height],
        annotations=[]
    )
