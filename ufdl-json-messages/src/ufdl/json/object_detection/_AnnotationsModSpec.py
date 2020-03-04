from typing import List

from wai.json.object import StrictJSONObject
from wai.json.object.property import ArrayProperty

from ._Annotation import Annotation


class AnnotationsModSpec(StrictJSONObject['AnnotationsModSpec']):
    """
    Represents a modification to the annotations of an image.
    """
    # The annotations to set on the image
    annotations: List[Annotation] = ArrayProperty(
        element_property=Annotation.as_property()
    )
