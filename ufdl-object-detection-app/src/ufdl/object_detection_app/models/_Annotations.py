from json import loads
from typing import Set

from django.db import models

from ufdl.json.object_detection import Image

from wai.json.raw import RawJSONObject

from ..apps import UFDLObjectDetectionAppConfig


class AnnotationsQuerySet(models.QuerySet):
    """
    Represents a query-set of the annotations for images in an
    object-detection data-set.
    """
    def for_file(self, filename: str) -> 'AnnotationsQuerySet':
        """
        Filters the query-set to those annotations that are for a particular file.

        :param filename:    The name of the file to filter for.
        :return:            The filtered query-set.
        """
        return self.filter(filename=filename)


class Annotations(models.Model):
    """
    Represents the annotations for a single image in an object-detection
    data-set.
    """
    # The data-set the annotations belong to
    dataset = models.ForeignKey(
        f"{UFDLObjectDetectionAppConfig.label}.ObjectDetectionDataset",
        on_delete=models.DO_NOTHING,
        related_name="annotations"
    )

    # The name of the image the annotations are for
    filename = models.CharField(max_length=200,
                                editable=False)

    # The JSON string encoding the annotations
    annotations = models.TextField()

    objects = AnnotationsQuerySet.as_manager()

    @property
    def image(self) -> Image:
        """
        Creates an Image object from this set of annotations.
        """
        return Image.from_json_string(self.annotations)

    @property
    def raw_json(self) -> RawJSONObject:
        """
        Loads the set of annotations as raw JSON.
        """
        return loads(self.annotations)

    @property
    def labels(self) -> Set[str]:
        """
        The set of labels in these annotations.
        """
        return set(
            annotation['label']
            for annotation in self.raw_json['annotations']
        )

    class Meta:
        constraints = [
            # Ensure that each filename is only stored once
            models.UniqueConstraint(name="unique_annotations_per_image",
                                    fields=["dataset", "filename"])
        ]
