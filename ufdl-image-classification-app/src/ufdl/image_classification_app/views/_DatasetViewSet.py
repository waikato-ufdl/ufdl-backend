from ufdl.core_app.permissions import IsMember, MemberHasWritePermission
from ufdl.core_app.views import DatasetViewSet as CoreDatasetViewSet

from ..models import ImageClassificationDataset
from ..serialisers import DatasetSerialiser
from .mixins import CategoriesViewSet


class DatasetViewSet(CategoriesViewSet, CoreDatasetViewSet):
    queryset = ImageClassificationDataset.objects.all()
    serializer_class = DatasetSerialiser

    permission_classes = dict(
        get_categories=IsMember,
        modify_categories=MemberHasWritePermission,
        **CoreDatasetViewSet.permission_classes
    )
