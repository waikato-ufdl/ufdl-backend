from ufdl.core_app.serialisers import DatasetSerialiser as CoreDatasetSerialiser

from ..models import ImageClassificationDataset


class DatasetSerialiser(CoreDatasetSerialiser):
    class Meta(CoreDatasetSerialiser.Meta):
        model = ImageClassificationDataset

    def to_representation(self, instance):
        # Get the base representation
        representation = super().to_representation(instance)

        # Add the categories file as a field
        representation["categories"] = instance.get_categories().to_raw_json()

        return representation
