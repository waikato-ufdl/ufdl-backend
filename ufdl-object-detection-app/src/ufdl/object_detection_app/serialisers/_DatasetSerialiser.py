from ufdl.core_app.serialisers import DatasetSerialiser as CoreDatasetSerialiser

from ..models import ObjectDetectionDataset


class DatasetSerialiser(CoreDatasetSerialiser):
    class Meta(CoreDatasetSerialiser.Meta):
        model = ObjectDetectionDataset
