from ufdl.core_app.serialisers import DatasetSerialiser as CoreDatasetSerialiser

from ..models import ObjectDetectionDataset


class DatasetSerialiser(CoreDatasetSerialiser):
    class Meta(CoreDatasetSerialiser.Meta):
        model = ObjectDetectionDataset

    def to_representation(self, instance):
        # Get the base representation
        representation = super().to_representation(instance)

        # Add the categories file as a field
        representation["annotations"] = instance.get_annotations().to_raw_json()

        return representation
