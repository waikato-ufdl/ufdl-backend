from ...models.models import FinalModel
from ...serialisers.models import FinalModelSerialiser
from ._ModelViewSet import ModelViewSet


class FinalModelViewSet(ModelViewSet):
    queryset = FinalModel.objects.all()
    serializer_class = FinalModelSerialiser
