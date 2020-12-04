from typing import Iterator, List, Optional

from django.db import models

from ufdl.annotation_utils.image_segmentation import annotations_iterator

from ufdl.core_app.exceptions import BadArgumentValue
from ufdl.core_app.models import Dataset, DatasetQuerySet
from ufdl.core_app.models.files import File

from wai.annotations.domain.image.segmentation import ImageSegmentationInstance

from ._SegmentationLayerImage import SegmentationLayerImage


class ImageSegmentationDatasetQuerySet(DatasetQuerySet):
    pass


class ImageSegmentationDataset(Dataset):
    # The labels of the dataset (new-line separated)
    labels = models.TextField()

    objects = ImageSegmentationDatasetQuerySet.as_manager()

    @classmethod
    def domain_code(cls) -> str:
        return "is"

    def can_merge(self, other) -> Optional[str]:
        # Test any higher-priority conditions
        super_reason = super().can_merge(other)

        # If they failed, report them
        if super_reason is not None:
            return super_reason

        assert isinstance(other, ImageSegmentationDataset)

        # Make sure the other data-set has the same labels as us
        return (
            None
            if self.get_labels() == other.get_labels() else
            "Source data-set has different labels to target"
        )

    def merge_annotations(self, other, files):
        for source_file, target_file in files:
            # Delete any existing layers from the target file
            self.annotations.for_file(target_file.filename).delete()

            # Add the layers from the source file to this data-set
            for layer in other.annotations.for_file(source_file.filename).all():
                SegmentationLayerImage(
                    dataset=self,
                    filename=target_file.filename,
                    label=layer.label,
                    mask=layer.mask
                ).save()

    def clear_annotations(self):
        self.annotations.delete()

    def delete_file(self, filename: str):
        # Delete the file as usual
        file = super().delete_file(filename)

        # Remove the file's annotation layers as well
        self.annotations.for_file(filename).delete()

        return file

    def get_annotations_iterator(self) -> Iterator[ImageSegmentationInstance]:
        return annotations_iterator(
            self.iterate_filenames(),
            self.get_labels(),
            self.get_layer,
            self.get_file
        )

    def get_layer(self, filename: str, label: str) -> Optional[bytes]:
        """
        Gets the layer mask for the given filename/label.

        :param filename:
                    The file the mask is for.
        :param label:
                    The label of the mask.
        :return:
                    The mask data.
        """
        # Make sure the filename is valid
        self.has_file(filename, throw=True)

        # Must be a valid label
        if not self.has_label(label):
            raise BadArgumentValue("set_layer", "label", label, str(self.get_labels()))

        # Get the existing layer instance
        layer = self.annotations.for_file(filename).for_label(label).first()

        return (
            layer.mask.get_data()
            if layer is not None else
            None
        )

    def set_layer(self, filename: str, label: str, mask: bytes):
        """
        Adds/updates the mask for a layer of a particular file.

        :param filename:
                    The name of the file the mask layer is for.
        :param label:
                    The label for the layer.
        :param mask:
                    The binary mask data.
        """
        # Make sure the filename is valid
        self.has_file(filename, throw=True)

        # Must be a valid label
        if not self.has_label(label):
            raise BadArgumentValue("set_layer", "label", label, str(self.get_labels()))

        # Create a file reference for the mask
        mask_file = File.create(mask)

        # Get the existing layer instance
        layer = self.annotations.for_file(filename).for_label(label).first()

        # If the layer already exists, update it's mask
        if layer is not None:
            original_mask_file = layer.mask
            layer.mask = mask_file
            original_mask_file.delete()

        # If the layer doesn't exist already, create it
        else:
            layer = SegmentationLayerImage(
                dataset=self,
                filename=filename,
                label=label,
                mask=mask_file
            )

        # Save the new/updated layer
        layer.save()

    def get_labels(self) -> List[str]:
        """
        Gets the canonically-ordered list of labels for this data-set.

        :return:
                    The list of labels.
        """
        return (
            self.labels.split("\n")
            if self.labels != "" else
            []
        )

    def set_labels(self, labels: List[str]):
        """
        Sets the labels for this data-set.

        :param labels:
                    The labels.
        """
        assert len(labels) == len(set(labels)), f"Duplicate labels in: " + ", ".join(labels)

        # Set the labels text field
        self.labels = (
            ""
            if len(labels) == 0 else
            "\n".join(labels)
        )
        self.save(update_fields=["labels"])

        # Remove any annotations that aren't in the label set
        self.annotations.filter(~models.Q(label__in=labels)).delete()

    def has_label(self, label: str) -> bool:
        """
        Whether this data-set has a given label.

        :param label:
                    The label to check for.
        :return:
                    True if the label is valid, False if not.
        """
        return label in self.get_labels()
