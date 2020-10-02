from ufdl.core_app.serialisers import DatasetSerialiser as CoreDatasetSerialiser

from ..models import ImageClassificationDataset


class DatasetSerialiser(CoreDatasetSerialiser):
    class Meta(CoreDatasetSerialiser.Meta):
        model = ImageClassificationDataset
