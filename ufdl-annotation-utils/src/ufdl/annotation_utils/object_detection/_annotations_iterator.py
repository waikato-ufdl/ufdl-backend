from typing import Iterator, Callable, Iterable, Optional, Tuple

from ufdl.json.object_detection import Image

from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance

from ._image_to_annotations_internal_format import image_to_annotations_internal_format


def annotations_iterator(
        filenames: Iterable[str],
        image_supplier: Callable[[str], Iterable[Tuple[str, bytes, Optional[Image]]]]
) -> Iterator[ImageObjectDetectionInstance]:
    """
    Creates an iterator over the images in an annotations file in
    the format expected by wai.annotations.

    :param filenames:
                The names of the files in the dataset.
    :param image_supplier:
                A supplier of:
                - a filename,
                - image data, and,
                - optional descriptions
                for files.
    :return:
                The iterator.
    """

    # Process each known image file
    for filename in filenames:
        for augmented_filename, image_data, image in image_supplier(filename):
            yield image_to_annotations_internal_format(
                image,
                augmented_filename,
                image_data
            )
