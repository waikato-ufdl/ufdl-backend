from ...models.models import PreTrainedModel
from ._ModelSerialiser import ModelSerialiser


class PreTrainedModelSerialiser(ModelSerialiser):
    class Meta(ModelSerialiser.Meta):
        model = PreTrainedModel
        fields = ["url", "description"] + ModelSerialiser.Meta.fields
