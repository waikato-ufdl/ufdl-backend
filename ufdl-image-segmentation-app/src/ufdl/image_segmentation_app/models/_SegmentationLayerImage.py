from django.db import models

from ufdl.core_app.apps import UFDLCoreAppConfig
from ufdl.core_app.util import accumulate_delete

from ..apps import UFDLImageSegmentationAppConfig


class SegmentationLayerImageQuerySet(models.QuerySet):
    """
    Represents a query-set of the annotation images.
    """
    def for_file(self, filename: str) -> 'SegmentationLayerImageQuerySet':
        """
        Filters the query-set to those annotations that are for a particular file.

        :param filename:
                    The name of the file to filter for.
        :return:
                    The filtered query-set.
        """
        return self.filter(filename=filename)

    def for_label(self, label: str) -> 'SegmentationLayerImageQuerySet':
        """
        Filters the query-set to those annotations that are for a particular label.

        :param label:
                    The label.
        :return:
                    The filtered query-set.
        """
        return self.filter(label=label)

    def delete(self):
        # Delete all file references as well so they don't leak
        delete_results = [
            layer.mask.delete()
            for layer in self.all()
        ]

        # Delete ourselves
        super_result = super().delete()

        # Accumulate the results
        for delete_result in delete_results:
            super_result = accumulate_delete(super_result, delete_result)

        return super_result


class SegmentationLayerImage(models.Model):
    """
    Represents the segment for a single label for a single image in
    an image-segmentation data-set.
    """
    # The data-set the annotations belong to
    dataset = models.ForeignKey(
        f"{UFDLImageSegmentationAppConfig.label}.ImageSegmentationDataset",
        on_delete=models.DO_NOTHING,
        related_name="annotations"
    )

    # The name of the image the annotations are for
    filename = models.CharField(
        max_length=200,
        editable=False
    )

    # The label for this layer
    label = models.TextField()

    # The binary image file containing the mask for the label
    mask = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.File",
        on_delete=models.DO_NOTHING,
        related_name="+"
    )

    objects = SegmentationLayerImageQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each filename is only stored once
            models.UniqueConstraint(
                name="unique_segmentation_layers",
                fields=["dataset", "filename", "label"]
            )
        ]

    def delete(self, using=None, keep_parents=False):
        # Delete the file as well
        delete_result = self.mask.delete()

        # Delete ourselves
        self_result = super().delete(using, keep_parents)

        return accumulate_delete(delete_result, self_result)
