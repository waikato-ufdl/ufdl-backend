from ufdl.core_app.permissions import IsMember, WriteOrNodeExecutePermission
from ufdl.core_app.views import DatasetViewSet as CoreDatasetViewSet

from ..models import SpeechDataset
from ..serialisers import DatasetSerialiser
from .mixins import TranscriptionsViewSet


class DatasetViewSet(TranscriptionsViewSet, CoreDatasetViewSet):
    queryset = SpeechDataset.objects.all()
    serializer_class = DatasetSerialiser

    permission_classes = dict(
        get_transcriptions=IsMember,
        get_transcription_for_file=IsMember,
        set_transcription_for_file=WriteOrNodeExecutePermission,
        **CoreDatasetViewSet.permission_classes
    )
