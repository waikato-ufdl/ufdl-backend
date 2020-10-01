from json import loads, dumps
from typing import List, Optional, Iterator

from ufdl.annotation_utils.object_detection import image_from_file, annotations_iterator

from ufdl.core_app.models import Dataset, DatasetQuerySet

from ufdl.json.object_detection import AnnotationsFile, Annotation, Image

from wai.annotations.core.instance import Instance

from wai.json.raw import RawJSONObject, RawJSONArray


class ObjectDetectionDatasetQuerySet(DatasetQuerySet):
    pass


class ObjectDetectionDataset(Dataset):
    objects = ObjectDetectionDatasetQuerySet.as_manager()

    def __init__(self, *args, **kwargs):
        # Initialise as usual
        super().__init__(*args, **kwargs)

        # Set a default of no categories
        if self.unstructured == "":
            self.unstructured = "{}"

        # Make sure the unstructured data is valid
        AnnotationsFile.validate_json_string(self.unstructured)

    @classmethod
    def domain_code(cls) -> str:
        return "od"

    def merge_annotations(self, other, files):
        # Load the annotations files
        self_annotations_file = self.get_annotations()
        other_annotations_file = other.get_annotations()

        # Overwrite the annotations for the target files
        for source_file, target_file in files:
            self_annotations_file[target_file.filename] = other_annotations_file[source_file.filename]

        # Save the annotations
        self.set_annotations(self_annotations_file)

    def delete_file(self, filename: str):
        # Delete the file as usual
        file = super().delete_file(filename)

        # Remove the file from the categories as well
        annotations = self.get_annotations()
        if annotations.has_property(filename):
            annotations.delete_property(filename)
            self.set_annotations(annotations)

        return file

    def get_annotations_iterator(self) -> Optional[Iterator[Instance]]:
        # Get the annotations file
        annotations_file = self.get_annotations()

        # Create a supplier function for getting the image description for a file
        def get_image(filename: str) -> Optional[Image]:
            if not annotations_file.has_property(filename):
                return None

            return annotations_file[filename]

        return annotations_iterator(self.iterate_filenames(), get_image, self.get_file)

    def get_annotations(self) -> AnnotationsFile:
        """
        Gets the annotations of this object detection data-set.

        :return:    The annotations for each image.
        """
        return AnnotationsFile.from_json_string(self.unstructured)

    def get_annotations_raw(self) -> RawJSONObject:
        """
        Gets the annotations of this object detection data-set, in raw JSON format.

        :return:    The annotations for each image.
        """
        return loads(self.unstructured)

    def set_annotations(self, annotations_file: AnnotationsFile):
        """
        Sets the annotations to the given file.

        :param annotations_file:    The new annotations file.
        """
        self.unstructured = annotations_file.to_json_string()
        self.save()

    def set_annotations_raw(self, annotations_file: RawJSONObject):
        """
        Sets the annotations to the given file.

        :param annotations_file:    The new annotations file, in raw JSON format.
        """
        self.unstructured = dumps(annotations_file)
        self.save()

    def get_annotations_for_image(self, filename: str) -> RawJSONArray:
        """
        Sets the annotations for an image.

        :param filename:        The filename of the image.
        :return:                The list of image annotations.
        """
        # Get the annotations file
        annotations_file = self.get_annotations_raw()

        # Call this to check the file exists
        self.get_named_file_record(filename)

        # If there are no annotations for the image, return an empty list
        if filename not in annotations_file:
            return []

        return annotations_file[filename]['annotations']

    def set_annotations_for_image(self, filename: str, annotations: RawJSONArray):
        """
        Sets the annotations for an image.

        :param filename:        The filename of the image.
        :param annotations:     The annotations to set against the image.
        """

        # Get the annotations file
        annotations_file = self.get_annotations_raw()

        # Get the reference to the file we are annotating
        file = self.get_named_file_record(filename)

        # Addition mode
        if len(annotations) > 0:
            # Create the property if not already existing
            if filename not in annotations_file:
                annotations_file[filename] = image_from_file(file.filename, file.get_data()).to_raw_json()

            # Replace the annotations for the image
            annotations_file[filename]['annotations'] = annotations

        # Deletion mode
        else:
            if filename in annotations_file:
                del annotations_file[filename]

        # Save the annotations
        self.set_annotations_raw(annotations_file)
