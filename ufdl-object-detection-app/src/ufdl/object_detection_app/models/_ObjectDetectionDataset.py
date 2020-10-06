from json import dumps
from typing import Optional, Iterator, Set

from ufdl.annotation_utils.object_detection import image_from_file, annotations_iterator

from ufdl.core_app.models import Dataset, DatasetQuerySet

from ufdl.json.object_detection import AnnotationsFile, Annotation, Image

from wai.annotations.core.instance import Instance

from wai.json.raw import RawJSONObject, RawJSONArray

from ._Annotations import Annotations


class ObjectDetectionDatasetQuerySet(DatasetQuerySet):
    pass


class ObjectDetectionDataset(Dataset):
    objects = ObjectDetectionDatasetQuerySet.as_manager()

    @classmethod
    def domain_code(cls) -> str:
        return "od"

    def merge_annotations(self, other, files):
        # Overwrite the annotations for the target files
        for source_file, target_file in files:
            target_annotation = self._get_or_create_annotations(target_file)
            target_annotation.annotations = other.annotations.for_file(source_file).first().annotations
            target_annotation.save()

    def clear_annotations(self):
        self.annotations.all().delete()

    def delete_file(self, filename: str):
        # Delete the file as usual
        file = super().delete_file(filename)

        # Remove the file from the annotations as well
        self.annotations.for_file(filename).delete()

        return file

    def get_annotations_iterator(self) -> Optional[Iterator[Instance]]:
        # Create a supplier function for getting the image description for a file
        def get_image(filename: str) -> Optional[Image]:
            annotation = self.annotations.for_file(filename).first()

            if annotation is None:
                return None

            return annotation.image

        return annotations_iterator(self.iterate_filenames(), get_image, self.get_file)

    def get_annotations(self) -> AnnotationsFile:
        """
        Gets the annotations of this object detection data-set.

        :return:    The annotations for each image.
        """
        annotations_file = AnnotationsFile()

        for annotation in self.annotations.all():
            annotations_file[annotation.filename] = annotation.image

        return annotations_file

    def get_annotations_raw(self) -> RawJSONObject:
        """
        Gets the annotations of this object detection data-set, in raw JSON format.

        :return:    The annotations for each image.
        """
        raw = {}

        for annotation in self.annotations.all():
            raw[annotation.filename] = annotation.raw_json

        return raw

    def get_labels(self) -> Set[str]:
        """
        Gets the labels that are present in this data-set.

        :return:    The list of labels.
        """
        # Create an empty set to buffer the labels in
        labels = set()

        # Add the labels for each image into the buffer
        for annotation in self.annotations.all():
            labels.update(annotation.labels)

        return labels

    def set_annotations(self, annotations_file: AnnotationsFile):
        """
        Sets the annotations to the given file.

        :param annotations_file:    The new annotations file.
        """
        # Remove any existing annotations
        self.clear_annotations()

        for filename in annotations_file:
            self.set_annotations_for_image(filename, annotations_file.get_property_as_raw_json(filename))

    def set_annotations_raw(self, annotations_file: RawJSONObject):
        """
        Sets the annotations to the given file.

        :param annotations_file:    The new annotations file, in raw JSON format.
        """
        # Remove any existing annotations
        self.clear_annotations()

        for filename, annotations in annotations_file.items():
            self.set_annotations_for_image(filename, annotations)

    def get_annotations_for_image(self, filename: str) -> RawJSONArray:
        """
        Sets the annotations for an image.

        :param filename:        The filename of the image.
        :return:                The list of image annotations.
        """
        # Call this to check the file exists
        self.get_named_file_record(filename)

        # Get the annotations file
        annotations = self.annotations.for_file(filename).first()

        # If there are no annotations for the image, return an empty list
        if annotations is None:
            return []

        return annotations.raw_json['annotations']

    def set_annotations_for_image(self, filename: str, annotations: RawJSONArray):
        """
        Sets the annotations for an image.

        :param filename:        The filename of the image.
        :param annotations:     The annotations to set against the image.
        """
        # Get the reference to the file we are annotating
        file = self.get_named_file_record(filename)

        # Addition mode
        if len(annotations) > 0:
            # Get the annotations object
            annotation = self._get_or_create_annotations(filename)

            # Create an image object for the annotations
            image = image_from_file(file.filename, file.get_data()).to_raw_json()

            # Set the annotations
            image['annotations'] = annotations

            # Serialise the image
            annotation.annotations = dumps(image)

            # Save
            annotation.save()

        # Deletion mode
        else:
            self.annotations.for_file(filename).delete()

    def _get_or_create_annotations(self, filename: str) -> Annotations:
        """
        Gets the existing annotations object for the given file,
        or creates it if it does not already exist.

        :param filename:    The file to get the annotations for.
        :return:            The annotations.
        """
        # Try to get the existing annotations
        annotations = self.annotations.for_file(filename).first()

        # Create a new object if it doesn't already exist
        if annotations is None:
            annotations = Annotations(
                dataset=self,
                filename=filename
            )

        return annotations
