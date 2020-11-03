from typing import Iterator, Callable, Iterable, List

from wai.annotations.domain.image import Image
from wai.annotations.domain.image.classification import ImageClassificationInstance


def annotations_iterator(filenames: Iterable[str],
                         categories_supplier: Callable[[str], List[str]],
                         image_data_supplier: Callable[[str], bytes]) -> Iterator[ImageClassificationInstance]:
    """
    Creates an iterator over the images in an annotations file in
    the format expected by wai.annotations.

    :param filenames:               An iterator over the filenames in the dataset.
    :param categories_supplier:     A supplier of categories for given image filenames.
    :param image_data_supplier:     A callable that takes the filename of an image and returns
                                    the image's data.
    :return:                        The iterator.
    """

    # Process each known image file
    for filename in filenames:
        # Get the categories for this file
        categories = categories_supplier(filename)

        # wai.annotations expects one category per image, but the backend can have multiple,
        # so just use the first
        category = "" if len(categories) == 0 else categories[0]

        yield ImageClassificationInstance(
            Image.from_file_data(filename, image_data_supplier(filename)),
            category
        )
