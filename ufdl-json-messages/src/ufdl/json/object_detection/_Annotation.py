from wai.annotations.core.utils import get_object_prefix, get_object_label, set_object_label, set_object_prefix

from wai.common.adams.imaging.locateobjects import LocatedObject

from wai.json.object import StrictJSONObject, Absent
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

    @staticmethod
    def from_located_object(located_object: LocatedObject) -> 'Annotation':
        """
        Creates an annotation from a located object.

        :param located_object:  The located object.
        :return:                The annotation.
        """
        return Annotation(x=located_object.x,
                          y=located_object.y,
                          width=located_object.width,
                          height=located_object.height,
                          polygon=(Polygon.from_polygon(located_object.get_actual_polygon())
                                   if located_object.has_polygon() else Absent),
                          label=get_object_label(located_object),
                          prefix=get_object_prefix(located_object, Absent))

    def to_located_object(self) -> LocatedObject:
        """
        Creates a located object from this annotation.

        :return:    The located object.
        """
        # Create the basic located object
        located_object = LocatedObject(self.x, self.y, self.width, self.height)

        # Add the polygon if present
        if self.polygon is not Absent:
            located_object.set_polygon(self.polygon.to_polygon())

        # Set the label
        set_object_label(located_object, self.label)

        # Set the prefix if present
        if self.prefix is not Absent:
            set_object_prefix(located_object, self.prefix)

        return located_object
