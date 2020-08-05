from ...models.models import FinalModel
from ._ModelSerialiser import ModelSerialiser


class FinalModelSerialiser(ModelSerialiser):
    class Meta(ModelSerialiser.Meta):
        model = FinalModel
        fields = ["base_model"] + ModelSerialiser.Meta.fields
