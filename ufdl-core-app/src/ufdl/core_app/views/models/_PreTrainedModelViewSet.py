from ...models.models import PreTrainedModel
from ...serialisers.models import PreTrainedModelSerialiser
from ._ModelViewSet import ModelViewSet


class PreTrainedModelViewSet(ModelViewSet):
    queryset = PreTrainedModel.objects.all()
    serializer_class = PreTrainedModelSerialiser
