from ufdl.core_app.permissions import WriteOrNodeExecutePermission, IsMember
from ufdl.core_app.views import DatasetViewSet as CoreDatasetViewSet

from ..models import ObjectDetectionDataset
from ..serialisers import DatasetSerialiser
from .mixins import AnnotationsViewSet


class DatasetViewSet(AnnotationsViewSet, CoreDatasetViewSet):
    queryset = ObjectDetectionDataset.objects.all()
    serializer_class = DatasetSerialiser

    permission_classes = dict(
        get_annotations=IsMember,
        get_annotations_for_image=IsMember,
        set_annotations_for_image=WriteOrNodeExecutePermission,
        delete_annotations_for_image=WriteOrNodeExecutePermission,
        get_labels=IsMember,
        **CoreDatasetViewSet.permission_classes
    )
