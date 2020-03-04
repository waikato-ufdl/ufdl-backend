from typing import Iterator

from ufdl.core_app.models.mixins import FileContainerModel

from wai.annotations.core import InternalFormat as AnnotationsInternalFormat

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

    def annotations_iterator(self, file_supplier: FileContainerModel) -> Iterator[AnnotationsInternalFormat]:
        """
        Creates an iterator over the images in the dataset in
        the format expected by wai.annotations.

        :param file_supplier:   The model containing the image files.
        :return:                The iterator.
        """
        # Process each known image file
        for filename in self.properties():
            # Get the data corresponding to the filename
            data = file_supplier.files.all().with_filename(filename).first().get_data()

            yield self[filename].to_annotations_internal_format(filename, data)
