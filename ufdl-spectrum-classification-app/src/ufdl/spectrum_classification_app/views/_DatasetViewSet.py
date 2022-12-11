from ufdl.core_app.permissions import IsMember, WriteOrNodeExecutePermission
from ufdl.core_app.views import DatasetViewSet as CoreDatasetViewSet

from ..models import SpectrumClassificationDataset
from ..serialisers import DatasetSerialiser
from .mixins import CategoriesViewSet


class DatasetViewSet(CategoriesViewSet, CoreDatasetViewSet):
    queryset = SpectrumClassificationDataset.objects.all()
    serializer_class = DatasetSerialiser

    permission_classes = dict(
        get_categories=IsMember,
        get_categories_for_file=IsMember,
        modify_categories=WriteOrNodeExecutePermission,
        set_categories=WriteOrNodeExecutePermission,
        **CoreDatasetViewSet.permission_classes
    )
