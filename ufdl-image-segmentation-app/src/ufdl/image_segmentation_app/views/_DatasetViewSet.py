from ufdl.core_app.permissions import IsMember, WriteOrNodeExecutePermission
from ufdl.core_app.views import DatasetViewSet as CoreDatasetViewSet

from ..models import ImageSegmentationDataset
from ..serialisers import DatasetSerialiser
from .mixins import SegmentationLayersViewSet


class DatasetViewSet(SegmentationLayersViewSet, CoreDatasetViewSet):
    queryset = ImageSegmentationDataset.objects.all()
    serializer_class = DatasetSerialiser

    permission_classes = dict(
        get_layer=IsMember,
        set_layer=WriteOrNodeExecutePermission,
        get_labels=IsMember,
        set_labels=WriteOrNodeExecutePermission,
        **CoreDatasetViewSet.permission_classes
    )
