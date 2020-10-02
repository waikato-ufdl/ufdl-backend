from ufdl.core_app.serialisers import DatasetSerialiser as CoreDatasetSerialiser

from ..models import SpeechDataset


class DatasetSerialiser(CoreDatasetSerialiser):
    class Meta(CoreDatasetSerialiser.Meta):
        model = SpeechDataset
