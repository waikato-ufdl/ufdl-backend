import numpy as np
from typing import Iterator, Callable, Iterable, List, Optional

from wai.annotations.domain.image import Image
from wai.annotations.domain.image.segmentation import (
    ImageSegmentationInstance,
    ImageSegmentationAnnotation
)


def annotations_iterator(
        filenames: Iterable[str],
        labels: List[str],
        layer_image_supplier: Callable[[str, str], Optional[bytes]],
        image_data_supplier: Callable[[str], bytes]
) -> Iterator[ImageSegmentationInstance]:
    """
    Creates an iterator over the images in an image-segmentation dataset in
    the format expected by wai.annotations.

    :param filenames:
                An iterator over the filenames in the dataset.
    :param labels:
                The labels for this data-set.
    :param layer_image_supplier:
                A supplier of the layer image for a given filename/label.
    :param image_data_supplier:
                A callable that takes the filename of an image and returns
                the image's data.
    :return:
                The iterator.
    """
    # Create an index lookup for the labels
    label_lookup = {
        label: index
        for index, label in enumerate(labels, 1)
    }

    # Process each known image file
    for filename in filenames:
        # Load the data image
        data_image = Image.from_file_data(filename, image_data_supplier(filename))

        # Create a segmentation annotation
        annotation = ImageSegmentationAnnotation(labels, data_image.size)

        # Process labels in reverse-order, so lower-indexed labels take priority
        # (i.e. overwrite) higher-indexed labels
        for label in reversed(labels):
            # Get the layer image data for this label
            layer_image_data = layer_image_supplier(filename, label)

            # Skip missing layers
            if layer_image_data is None:
                continue

            # Load the label image
            layer_image = Image.from_file_data("example.png", layer_image_data).pil_image

            # The image must be binary
            if layer_image.mode != "1":
                raise Exception(f"Label image is not binary ({layer_image.mode})")

            # Convert the image to 8-bit mode to separate pixels
            layer_image = layer_image.convert("L")

            # Extract an array of the required shape from the image
            mask = np.fromstring(layer_image.tobytes(), dtype=np.uint8)
            mask.resize(annotation.indices.shape)

            # Create a boolean array which selects the annotated pixels
            selector_array = mask != 0

            # Merge the current index set with the indices from this label
            annotation.indices = np.where(
                selector_array,
                np.uint16(label_lookup[label]),
                annotation.indices
            )

        yield ImageSegmentationInstance(data_image, annotation)
