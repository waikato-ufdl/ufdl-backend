from json import dumps

from typing import List, Optional, Set, Tuple, Union

from ufdl.core_app.exceptions import BadName, BadArgumentValue, BadArgumentType
from ufdl.core_app.models import Dataset, DatasetQuerySet, FileReference

from ufdl.json.object_detection import AnnotationsFile, Image, Video, ImageAnnotation, VideoAnnotation

from wai.json.object import Absent

from ._Annotation import Annotation
from ._Annotations import Annotations, AnnotationsQuerySet
from ._DatasetToLabel import DatasetToLabel
from ._DatasetToPrefix import DatasetToPrefix
from ._Label import Label
from ._Prefix import Prefix


class ObjectDetectionDatasetQuerySet(DatasetQuerySet):
    pass


class ObjectDetectionDataset(Dataset):
    objects = ObjectDetectionDatasetQuerySet.as_manager()

    @classmethod
    def domain_code(cls) -> str:
        return "od"

    @property
    def annotations(self) -> AnnotationsQuerySet:
        return Annotations.objects.filter(file__in=self.files.all())

    def merge_annotations(self, other, files):
        other: ObjectDetectionDataset = other.domain_specific
        # Overwrite the annotations for the target files
        for source_file, target_file in files:
            # Get the annotations container for the source file
            source_annotations = other._get_annotations_container(source_file)

            # If there is none, this file has no annotations
            if source_annotations is None:
                continue

            # Check if the annotations container for this file is already set,
            # and if so, ensure it is identical
            target_annotations = self._get_annotations_container(target_file)
            if target_annotations is not None:
                if (
                    target_annotations.format != source_annotations.format
                    or target_annotations.width != source_annotations.width
                    or target_annotations.height != source_annotations.height
                    or target_annotations.video_length != source_annotations.video_length
                ):
                    raise BadName(
                        target_file.filename,
                        f"File-type already set and differs from source file '{source_file.filename}'\n"
                        f"Source: format={source_annotations.format}, width={source_annotations.width}, height={source_annotations.height}, length={source_annotations.video_length}"
                        f"Target: format={target_annotations.format}, width={target_annotations.width}, height={target_annotations.height}, length={target_annotations.video_length}"
                    )
            else:
                # Create an identical container for the target file
                self.set_file_type(
                    target_file,
                    source_annotations.format,
                    source_annotations.width,
                    source_annotations.height,
                    source_annotations.video_length
                )

            # Get the list of annotations already set on the file
            current_annotations = self.get_annotations_for_file(target_file)

            # Append the annotations of the source file
            new_annotations = current_annotations + other.get_annotations_for_file(source_file)

            self.set_annotations_for_file(
                target_file,
                new_annotations
            )

    def clear_annotations(self):
        Annotation.objects.filter(container__in=self.annotations.all()).delete()

    def delete_file(self, filename: str):
        # Remove the annotations for the file
        self.annotations.for_file(filename).delete()

        # Delete the file as usual
        file = super().delete_file(filename)

        return file

    def add_label(self, label: str) -> Tuple[Label, DatasetToLabel]:
        """
        Adds a label to this dataset.

        :param label:
                    The label to add.
        """
        # See if the label already exists
        existing_label = Label.objects.filter(text=label).first()

        # If it doesn't exist, create it
        if existing_label is None:
            existing_label = Label(text=label)
            existing_label.save()

        # See if the dataset already has this label
        existing_label_ref = DatasetToLabel.objects.filter(dataset=self, label=existing_label).first()

        # Create the reference if not already there
        if existing_label_ref is None:
            existing_label_ref = DatasetToLabel(dataset=self, label=existing_label)
            existing_label_ref.save()

        return existing_label, existing_label_ref

    def remove_label(self, label: str):
        """
        Removes a label from this dataset.

        :param label:
            The label to remove.
        """
        # Get the label
        existing_label = self.labels.filter(text=label).first()

        # Abort if the label doesn't exist in this dataset
        if existing_label is None:
            return

        # Get this dataset's reference to the label
        label_reference = DatasetToLabel.objects.filter(
            dataset=self,
            label=existing_label
        ).first()

        # Delete any annotations using this label-reference
        Annotation.objects.filter(
            label_reference=label_reference
        ).delete()

        # Delete the label from this dataset
        label_reference.delete()

        # Try to delete the label as well
        existing_label.delete()

    def get_labels(self) -> Set[str]:
        """
        Gets the labels that are present in this data-set.

        :return:    The list of labels.
        """
        return set(label.text for label in self.labels.all())

    def add_prefix(self, prefix: str) -> Tuple[Prefix, DatasetToPrefix]:
        """
        Adds a prefix to this dataset.

        :param prefix:
                    The prefix to add.
        """
        # See if the prefix already exists
        existing_prefix = Prefix.objects.filter(text=prefix).first()

        # If it doesn't exist, create it
        if existing_prefix is None:
            existing_prefix = Prefix(text=prefix)
            existing_prefix.save()

        # See if the dataset already has this prefix
        existing_prefix_ref = DatasetToPrefix.objects.filter(dataset=self, prefix=existing_prefix).first()

        # Create the reference if not already there
        if existing_prefix_ref is None:
            existing_prefix_ref = DatasetToPrefix(dataset=self, prefix=existing_prefix)
            existing_prefix_ref.save()

        return existing_prefix, existing_prefix_ref

    def remove_prefix(self, prefix: str):
        """
        Removes a prefix from this dataset.

        :param prefix:
            The prefix to remove.
        """
        # Get the prefix
        existing_prefix = self.prefixes.filter(text=prefix).first()

        # Abort if the prefix doesn't exist in this dataset
        if existing_prefix is None:
            return

        # Get this dataset's reference to the prefix
        prefix_reference = DatasetToPrefix.objects.filter(
            dataset=self,
            prefix=existing_prefix
        ).first()

        # Delete any annotations using this prefix-reference
        Annotation.objects.filter(
            prefix_reference=prefix_reference
        ).delete()

        # Delete the prefix from this dataset
        prefix_reference.delete()

        # Try to delete the prefix as well
        existing_prefix.delete()

    def get_prefixes(self) -> Set[str]:
        """
        Gets the labels that are present in this data-set.

        :return:    The list of labels.
        """
        return set(prefix.text for prefix in self.prefixes.all())

    def get_file_type(
            self,
            file: Union[str, FileReference]
    ) -> Annotations:
        # Get the reference from the filename
        if isinstance(file, str):
            file = self.get_file_reference(file, throw=True)

        # Get the annotations for the file
        annotations = self.annotations.for_file(file).first()

        # Check the file-type is set
        if annotations is None:
            raise BadName(file.filename, "File-type not set")

        return annotations

    def set_file_type(
            self,
            file: Union[str, FileReference],
            format: Optional[str] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            video_length: Optional[float] = None
    ) -> Annotations:
        # Get the reference from the filename
        if isinstance(file, str):
            file = self.get_file_reference(file, throw=True)

        # It is an error to set the file-type twice
        if self.annotations.for_file(file).exists():
            raise BadName(file.filename, "File-type already set")

        # Create the annotations container
        annotations = Annotations(
            file=file,
            format=format,
            width=width,
            height=height,
            video_length=video_length
        )
        annotations.save()

        return annotations

    def _get_annotations_container(
            self,
            file: Union[str, FileReference, Annotations]
    ) -> Optional[Annotations]:
        """
        Normalises the file argument into an annotations container, throwing
        when the argument is not valid for this dataset.

        :param file:
                    The file to get the annotations container for.
        :return:
                    The annotations container.
        :raises BadName:
                    If [file] is a string that doesn't match a file in this dataset.
        :raises BadArgumentValue:
                    If [file] is a file-reference or annotations-container that doesn't belong
                    to this dataset, .
        """
        # Parse filenames to file-references
        if isinstance(file, str):
            file = self.get_file_reference(file, True)

        # Make sure we own the file reference
        elif isinstance(file, FileReference):
            if not self.files.all().filter(pk__exact=file.pk).exists():
                raise BadArgumentValue(
                    "get_annotations_container",
                    "file",
                    file.filename,
                    reason="File reference does not belong to dataset"
                )

        # Make sure the annotations are part of this dataset
        elif not self.annotations.all().filter(pk__exact=file.pk).exists():
            raise BadArgumentValue(
                "get_annotations_container",
                "file",
                file.filename,
                reason="Annotations container not owned by this dataset"
            )

        # Parse file-names/references into annotation containers
        annotations: Optional[Annotations] = (
            self.annotations.for_file(file).first()
            if isinstance(file, FileReference) else
            file
        )

        return annotations

    def add_annotation_to_file(
            self,
            file: Union[str, FileReference, Annotations],
            annotation: Union[ImageAnnotation, VideoAnnotation]
    ) -> Annotation:
        # Get the annotations container for the file
        annotations = self._get_annotations_container(file)

        # Raise an error if no container was found
        if annotations is None:
            raise BadArgumentValue(
                "get_annotations_container",
                "file",
                file.filename,
                reason="Has no container"
            )

        # Make sure the type of annotation matches the type of file
        if (
            (annotations.is_image and not isinstance(annotation, ImageAnnotation))
            or
            (annotations.is_video and not isinstance(annotation, VideoAnnotation))
        ):
            raise BadArgumentType(
                "add_annotation_to_file",
                "annotation",
                str(ImageAnnotation if annotations.is_image else VideoAnnotation),
                annotation
            )

        # Parse common parts of the annotation
        polygon = annotation.get_property_as_raw_json("polygon", validate=False)
        label, label_ref = self.add_label(annotation.label)
        prefix, prefix_ref = self.add_prefix(annotation.prefix)

        # Create the arguments to the Annotation instance
        annotation_args = dict(
            container=annotations,
            x=annotation.x,
            y=annotation.y,
            width=annotation.width,
            height=annotation.height,
            label_reference=label_ref,
            prefix_reference=prefix_ref
        )
        if polygon is not Absent:
            annotation_args["polygon"] = dumps(polygon)
        if isinstance(annotation, VideoAnnotation):
            annotation_args["time"] = annotation.time

        # Create the annotation instance
        annotation = Annotation(**annotation_args)
        annotation.save()

        return annotation

    def get_annotations_for_file(
            self,
            file: Union[str, FileReference, Annotations]
    ) -> Union[List[ImageAnnotation], List[VideoAnnotation]]:
        """
        Gets the annotations for an image or video.

        :param file:
                    The file for which to get the annotations.
        :return:
                    The list of annotations.
        """
        # Get the annotations container for the file
        annotations = self._get_annotations_container(file)

        # If there are no annotations for the image, return an empty list
        if annotations is None:
            return []

        return list(annotations.json.annotations)

    def clear_annotations_for_file(self, file: Union[str, FileReference]):
        """
        Deletes the annotations for a particular file.

        :param file:
                    The file for which to remove annotations.
        """
        annotations_container = self.annotations.for_file(file).first()
        if annotations_container is not None:
            annotations_container.annotations.all().delete()

    def set_annotations_for_file(
            self,
            file: Union[str, FileReference],
            annotations: Union[List[ImageAnnotation], List[VideoAnnotation]]):
        """
        Sets the annotations for a file.

        :param file:
                    The file for which to remove annotations.
        :param annotations:     The annotations to set against the image.
        """
        # Get the reference to the file we are annotating
        if isinstance(file, str):
            file = self.get_file_reference(file, True)

        # Clear any existing annotations from the file
        self.clear_annotations_for_file(file)

        for annotation in annotations:
            self.add_annotation_to_file(file, annotation)

    def set_annotations(self, annotations_file: AnnotationsFile):
        """
        Sets the annotations to the given file.

        :param annotations_file:    The new annotations file.
        """
        # Remove any existing annotations
        self.clear_annotations()

        for filename in annotations_file:
            file: Union[Image, Video] = annotations_file[filename]
            annotations = self.annotations.for_file(filename).first()
            if annotations is None:
                annotations = self.set_file_type(
                    filename,
                    file.format,
                    file.width,
                    file.height,
                    file.length if isinstance(file, Video) else None
                )

            self.set_annotations_for_file(filename, file.annotations)

    def get_annotations(self) -> AnnotationsFile:
        """
        Gets the current annotations for this dataset.

        :return:
                    The annotations as JSON.
        """
        return AnnotationsFile(
            **{
                annotations.filename: annotations.json
                for annotations in self.annotations
            }
        )