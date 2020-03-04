from rest_framework.permissions import AllowAny

from ufdl.core_app.views import DatasetViewSet as CoreDatasetViewSet

from ..models import ImageClassificationDataset
from ..serialisers import DatasetSerialiser
from .mixins import CategoriesViewSet


class DatasetViewSet(CategoriesViewSet, CoreDatasetViewSet):
    queryset = ImageClassificationDataset.objects.all()
    serializer_class = DatasetSerialiser

    permission_classes = dict(
        get_categories=[AllowAny],  # TODO: Change to a proper level of authorisation
        add_categories=[AllowAny],  # TODO: Change to a proper level of authorisation
        remove_categories=[AllowAny],  # TODO: Change to a proper level of authorisation
        **CoreDatasetViewSet.permission_classes
    )
