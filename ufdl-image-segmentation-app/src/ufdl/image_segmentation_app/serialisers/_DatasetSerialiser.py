from ufdl.core_app.serialisers import DatasetSerialiser as CoreDatasetSerialiser

from ..models import ImageSegmentationDataset


class DatasetSerialiser(CoreDatasetSerialiser):
    class Meta(CoreDatasetSerialiser.Meta):
        model = ImageSegmentationDataset
