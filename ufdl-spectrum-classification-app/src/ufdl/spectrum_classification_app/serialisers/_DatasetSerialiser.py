from ufdl.core_app.serialisers import DatasetSerialiser as CoreDatasetSerialiser

from ..models import SpectrumClassificationDataset


class DatasetSerialiser(CoreDatasetSerialiser):
    class Meta(CoreDatasetSerialiser.Meta):
        model = SpectrumClassificationDataset
