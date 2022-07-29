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
        set_annotations=WriteOrNodeExecutePermission,
        clear_annotations=WriteOrNodeExecutePermission,
        get_annotations_for_file=IsMember,
        add_annotations_to_file=WriteOrNodeExecutePermission,
        set_annotations_for_file=WriteOrNodeExecutePermission,
        delete_annotations_for_file=WriteOrNodeExecutePermission,
        get_labels=IsMember,
        add_labels=WriteOrNodeExecutePermission,
        delete_label=WriteOrNodeExecutePermission,
        get_prefixes=IsMember,
        add_prefixes=WriteOrNodeExecutePermission,
        delete_prefixes=WriteOrNodeExecutePermission,
        get_file_type=IsMember,
        set_file_type=WriteOrNodeExecutePermission,
        get_file_types=IsMember,

        **CoreDatasetViewSet.permission_classes
    )
