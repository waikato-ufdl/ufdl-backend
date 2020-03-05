from typing import Iterator, Callable

from ufdl.json.object_detection import AnnotationsFile

from wai.annotations.core import InternalFormat as AnnotationsInternalFormat

from ._image_to_annotations_internal_format import image_to_annotations_internal_format


def annotations_iterator(annotations_file: AnnotationsFile,
                         image_data_supplier: Callable[[str], bytes]) -> Iterator[AnnotationsInternalFormat]:
    """
    Creates an iterator over the images in an annotations file in
    the format expected by wai.annotations.

    :param annotations_file:        The annotations file.
    :param image_data_supplier:     A callable that takes the filename of an image and returns
                                    the image's data.
    :return:                        The iterator.
    """

    # Process each known image file
    for filename in annotations_file.properties():
        yield image_to_annotations_internal_format(annotations_file[filename],
                                                   filename,
                                                   image_data_supplier(filename))
