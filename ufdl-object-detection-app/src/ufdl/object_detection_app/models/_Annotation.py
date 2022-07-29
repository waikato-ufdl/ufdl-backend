from json import loads
from typing import Union

from django.db import models

from ufdl.json.object_detection import ImageAnnotation, VideoAnnotation

from ..apps import UFDLObjectDetectionAppConfig


class AnnotationQuerySet(models.QuerySet):
    """
    Represents a query-set of the annotations for a single image/video in an
    object-detection data-set.
    """
    def for_file(self, filename: str) -> 'AnnotationsQuerySet':
        """
        Filters the query-set to those annotations that are for a particular file.

        :param filename:    The name of the file to filter for.
        :return:            The filtered query-set.
        """
        return self.filter(file__file__name__filename=filename)


class Annotation(models.Model):
    """
    Represents the annotations for a single image in an object-detection
    data-set.
    """
    # The set of annotations this annotation belongs to
    container = models.ForeignKey(
        f"{UFDLObjectDetectionAppConfig.label}.Annotations",
        on_delete=models.DO_NOTHING,
        related_name="annotations"
    )

    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()

    # The timestamp in the video, null for images
    time = models.FloatField(null=True, default=None)

    # The optional polygon surrounding the annotation (just serialised JSON)
    polygon = models.TextField(null=True, default=None)

    label_reference = models.ForeignKey(
        f"{UFDLObjectDetectionAppConfig.label}.DatasetToLabel",
        on_delete=models.DO_NOTHING,
        related_name="annotations"
    )

    prefix_reference = models.ForeignKey(
        f"{UFDLObjectDetectionAppConfig.label}.DatasetToPrefix",
        on_delete=models.DO_NOTHING,
        related_name="annotations"
    )

    objects = AnnotationQuerySet.as_manager()

    @property
    def label(self) -> str:
        """
        The label of this annotation.
        """
        return self.label_reference.label

    @property
    def prefix(self) -> str:
        """
        The prefix of this annotation.
        """
        return self.prefix_reference.prefix

    @property
    def is_image(self) -> bool:
        return self.time is None

    @property
    def is_video(self) -> bool:
        return not self.is_image

    @property
    def json(self) -> Union[ImageAnnotation, VideoAnnotation]:
        if self.is_image:
            return self.json_image
        else:
            return self.json_video

    @property
    def json_image(self) -> ImageAnnotation:
        """
        TODO
        :return:
        """
        return ImageAnnotation(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            polygon=loads(self.polygon),
            label=self.label,
            prefix=self.prefix
        )

    @property
    def json_video(self) -> VideoAnnotation:
        """
        Creates an Image object from this set of annotations.
        """
        return VideoAnnotation(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            polygon=loads(self.polygon),
            label=self.label,
            prefix=self.prefix,
            time=self.time
        )
