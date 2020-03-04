from wai.json.object import StrictJSONObject
from wai.json.object.property import NumberProperty, StringProperty

from ._Polygon import Polygon


class Annotation(StrictJSONObject['Annotation']):
    """
    Represents a single annotation in an image.
    """
    # The bounding-box of the annotation
    x: int = NumberProperty(integer_only=True)
    y: int = NumberProperty(integer_only=True)
    width: int = NumberProperty(minimum=0, integer_only=True)
    height: int = NumberProperty(minimum=0, integer_only=True)

    # The optional polygon for mask annotations
    polygon: Polygon = Polygon.as_property(optional=True)

    # The annotations label
    label: str = StringProperty(min_length=1)

    # The optional prefix for the annotation
    prefix: str = StringProperty(min_length=1, optional=True, default="Object")
