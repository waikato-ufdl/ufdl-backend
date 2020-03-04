from typing import Iterator

from wai.annotations.core import InternalFormat as AnnotationsInternalFormat

from ..models import ObjectDetectionDataset
from ._image_to_annotations_internal_format import image_to_annotations_internal_format


def annotations_iterator(dataset: ObjectDetectionDataset) -> Iterator[AnnotationsInternalFormat]:
    """
    Creates an iterator over the images in a data-set in
    the format expected by wai.annotations.

    :param dataset:             The model containing the image files.
    :return:                    The iterator.
    """
    # Get the annotations file
    annotations_file = dataset.get_annotations()

    # Process each known image file
    for filename in annotations_file.properties():
        # Get the data corresponding to the filename
        data = dataset.files.all().with_filename(filename).first().get_data()

        yield image_to_annotations_internal_format(annotations_file[filename],
                                                   filename,
                                                   data)
