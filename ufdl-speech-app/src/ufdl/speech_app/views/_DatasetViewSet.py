from rest_framework.permissions import AllowAny

from ufdl.core_app.views import DatasetViewSet as CoreDatasetViewSet

from ..models import SpeechDataset
from ..serialisers import DatasetSerialiser
from .mixins import TranscriptionsViewSet


class DatasetViewSet(TranscriptionsViewSet, CoreDatasetViewSet):
    queryset = SpeechDataset.objects.all()
    serializer_class = DatasetSerialiser

    permission_classes = dict(
        get_transcriptions=[AllowAny],  # TODO: Change to a proper level of authorisation
        get_transcription_for_file=[AllowAny],  # TODO: Change to a proper level of authorisation
        set_transcription_for_file=[AllowAny],  # TODO: Change to a proper level of authorisation
        **CoreDatasetViewSet.permission_classes
    )
