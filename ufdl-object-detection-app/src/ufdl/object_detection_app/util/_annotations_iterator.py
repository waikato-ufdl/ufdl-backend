from typing import Iterator

from wai.annotations.core import InternalFormat as AnnotationsInternalFormat

from ._image_to_annotations_internal_format import image_to_annotations_internal_format


def annotations_iterator(dataset) -> Iterator[AnnotationsInternalFormat]:
    """
    Creates an iterator over the images in a data-set in
    the format expected by wai.annotations.

    :param dataset:             The dataset containing the image files.
    :return:                    The iterator.
    """
    # Local import to avoid circularity errors
    from ..models import ObjectDetectionDataset

    # Make sure the dataset is an object-detection dataset
    if not isinstance(dataset, ObjectDetectionDataset):
        raise TypeError("Dataset is not an object-detection dataset")

    # Get the annotations file
    annotations_file = dataset.get_annotations()

    # Process each known image file
    for filename in annotations_file.properties():
        # Get the data corresponding to the filename
        data = dataset.files.all().with_filename(filename).first().get_data()

        yield image_to_annotations_internal_format(annotations_file[filename],
                                                   filename,
                                                   data)
