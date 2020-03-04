from typing import List

from wai.common.geometry import Polygon as GeometricPolygon, Point

from wai.json.object import StrictJSONObject
from wai.json.object.property import ArrayProperty, NumberProperty


class Polygon(StrictJSONObject['Polygon']):
    """
    Represents a polygon mask for an annotation.
    """
    # The coordinates of the polygon
    points: List[List[int]] = ArrayProperty(
        element_property=ArrayProperty(
            element_property=NumberProperty(integer_only=True),
            min_elements=2, max_elements=2
        ),
        min_elements=3
    )

    def to_geometric_polygon(self) -> GeometricPolygon:
        """
        Converts this polygon into a geometric polygon.

        :return:    The geometric polygon.
        """
        return GeometricPolygon(*(Point(x, y) for x, y in self.points))

    @staticmethod
    def from_geometric_polygon(polygon: GeometricPolygon) -> 'Polygon':
        """
        Converts a geometric polygon into a Polygon record.

        :param polygon:     The geometric polygon.
        :return:            The Polygon record.
        """
        return Polygon(points=list([p.x, p.y] for p in polygon.points))
