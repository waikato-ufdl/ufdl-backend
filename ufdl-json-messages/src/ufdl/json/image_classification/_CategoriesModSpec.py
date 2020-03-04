from typing import List

from wai.json.object import StrictJSONObject
from wai.json.object.property import ArrayProperty, StringProperty


class CategoriesModSpec(StrictJSONObject['CategoriesModSpec']):
    """
    A specification of which images to modify the categories
    for, and which categories to modify for those images.
    """
    # The images to modify the categories for
    images: List[str] = ArrayProperty(
        element_property=StringProperty(min_length=1),
        min_elements=1,
        unique_elements=True
    )

    # The categories to add/remove from the images
    categories: List[str] = ArrayProperty(
        element_property=StringProperty(min_length=1),
        min_elements=1,
        unique_elements=True
    )
