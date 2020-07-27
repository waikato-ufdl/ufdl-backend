from ufdl.json.object_detection import Annotation

from wai.annotations.domain.image.object_detection.util import set_object_label, set_object_prefix

from wai.common.adams.imaging.locateobjects import LocatedObject

from wai.json.object import Absent


def located_object_from_annotation(annotation: Annotation) -> LocatedObject:
    """
    Creates a located object from an annotation.

    :param annotation:  The annotation.
    :return:            The located object.
    """
    # Create the basic located object
    located_object = LocatedObject(annotation.x, annotation.y, annotation.width, annotation.height)

    # Add the polygon if present
    if annotation.polygon is not Absent:
        located_object.set_polygon(annotation.polygon.to_geometric_polygon())

    # Set the label
    set_object_label(located_object, annotation.label)

    # Set the prefix if present
    if annotation.prefix is not Absent:
        set_object_prefix(located_object, annotation.prefix)

    return located_object
