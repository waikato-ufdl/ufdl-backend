from typing import List, Optional

from wai.json.object import StrictJSONObject, Absent
from wai.json.object.property import ArrayProperty, StringProperty, NumberProperty

from ._Annotation import Annotation


class Image(StrictJSONObject['Image']):
    """
    Represents a single image and its annotations.
    """
    # The image's format
    format: str = StringProperty(optional=True)

    # The image's dimensions
    dimensions: List[int] = ArrayProperty(
        element_property=NumberProperty(integer_only=True, minimum=1),
        min_elements=2, max_elements=2,
        optional=True
    )

    # The annotations of the image
    annotations: List[Annotation] = ArrayProperty(
        element_property=Annotation.as_property()
    )

    @property
    def width(self) -> Optional[int]:
        """
        Gets the width from the dimensions.

        :return:    The width, or None if not available.
        """
        if self.dimensions is not Absent:
            return self.dimensions[0]

    @property
    def height(self) -> Optional[int]:
        """
        Gets the height from the dimensions.

        :return:    The height, or None if not available.
        """
        if self.dimensions is not Absent:
            return self.dimensions[1]
