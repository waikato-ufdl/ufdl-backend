from wai.json.object import JSONObject
from wai.json.object.property import JSONObjectProperty

from ._Image import Image


class AnnotationsFile(JSONObject['AnnotationsFile']):
    """
    Defines the annotations for images in a dataset.
    """
    @classmethod
    def _additional_properties_validation(cls) -> JSONObjectProperty:
        return Image.as_property(optional=True)
