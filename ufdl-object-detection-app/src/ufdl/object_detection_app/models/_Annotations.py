from json import loads

from django.db import models

from ufdl.json.object_detection import Image

from wai.json.raw import RawJSONObject

from ..apps import UFDLObjectDetectionAppConfig


class AnnotationsQuerySet(models.QuerySet):
    def for_file(self, filename: str) -> 'AnnotationsQuerySet':
        """
        Filters the query-set to those annotations that are for a particular file.

        :param filename:    The name of the file to filter for.
        :return:            The filtered query-set.
        """
        return self.filter(filename=filename)


class Annotations(models.Model):
    dataset = models.ForeignKey(
        f"{UFDLObjectDetectionAppConfig.label}.ObjectDetectionDataset",
        on_delete=models.DO_NOTHING,
        related_name="annotations"
    )

    filename = models.CharField(max_length=200,
                                editable=False)

    annotations = models.TextField()

    objects = AnnotationsQuerySet.as_manager()

    @property
    def image(self) -> Image:
        return Image.from_json_string(self.annotations)

    @property
    def raw_json(self) -> RawJSONObject:
        return loads(self.annotations)

    class Meta:
        constraints = [
            # Ensure that each filename is only stored once
            models.UniqueConstraint(name="unique_annotations_per_image",
                                    fields=["dataset", "filename"])
        ]
