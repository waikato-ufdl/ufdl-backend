from ufdl.json.object_detection import Annotation, Polygon

from wai.annotations.domain.image.object_detection.util import get_object_prefix, get_object_label

from wai.common.adams.imaging.locateobjects import LocatedObject

from wai.json.object import Absent


def annotation_from_located_object(located_object: LocatedObject) -> Annotation:
    """
    Creates an annotation from a located object.

    :param located_object:  The located object.
    :return:                The annotation.
    """
    return Annotation(x=located_object.x,
                      y=located_object.y,
                      width=located_object.width,
                      height=located_object.height,
                      polygon=(Polygon.from_geometric_polygon(located_object.get_actual_polygon())
                               if located_object.has_polygon() else Absent),
                      label=get_object_label(located_object),
                      prefix=get_object_prefix(located_object, Absent))
