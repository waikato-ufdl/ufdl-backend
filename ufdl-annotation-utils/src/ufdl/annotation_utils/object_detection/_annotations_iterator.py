from typing import Iterator, Callable, Iterable, Optional

from ufdl.json.object_detection import AnnotationsFile, Image

from wai.annotations.domain.image.object_detection import ObjectDetectionInstance

from ._image_to_annotations_internal_format import image_to_annotations_internal_format


def annotations_iterator(filenames: Iterable[str],
                         image_supplier: Callable[[str], Optional[Image]],
                         image_data_supplier: Callable[[str], bytes]) -> Iterator[ObjectDetectionInstance]:
    """
    Creates an iterator over the images in an annotations file in
    the format expected by wai.annotations.

    :param filenames:               The names of the files in the dataset.
    :param image_supplier:          A supplier of image objects for files.
    :param image_data_supplier:     A callable that takes the filename of an image and returns
                                    the image's data.
    :return:                        The iterator.
    """

    # Process each known image file
    for filename in filenames:
        yield image_to_annotations_internal_format(image_supplier(filename),
                                                   filename,
                                                   image_data_supplier(filename))
