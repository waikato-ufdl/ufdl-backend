from wai.json.object import JSONObject
from wai.json.object.property import ArrayProperty, StringProperty


class CategoriesFile(JSONObject['CategoriesFile']):
    """
    Definition of a basic JSON file which holds a map
    from file names to an array of their categories.
    """
    @classmethod
    def _additional_properties_validation(cls) -> ArrayProperty:
        return ArrayProperty(
            element_property=StringProperty(min_length=1),
            unique_elements=True,  # Each category should only appear once
            optional=True,
            default=[]
        )
