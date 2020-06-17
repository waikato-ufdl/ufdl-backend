from ufdl.core_app.serialisers import DatasetSerialiser as CoreDatasetSerialiser

from ..models import SpeechDataset


class DatasetSerialiser(CoreDatasetSerialiser):
    class Meta(CoreDatasetSerialiser.Meta):
        model = SpeechDataset

    def to_representation(self, instance):
        # Get the base representation
        representation = super().to_representation(instance)

        # Add the categories file as a field
        representation["transcriptions"] = instance.get_transcriptions().to_raw_json()

        return representation
