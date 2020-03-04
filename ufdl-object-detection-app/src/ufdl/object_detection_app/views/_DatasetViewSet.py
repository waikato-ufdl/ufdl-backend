from rest_framework.permissions import AllowAny

from ufdl.core_app.views import DatasetViewSet as CoreDatasetViewSet

from ..models import ObjectDetectionDataset
from ..serialisers import DatasetSerialiser
from .mixins import AnnotationsViewSet


class DatasetViewSet(AnnotationsViewSet, CoreDatasetViewSet):
    queryset = ObjectDetectionDataset.objects.all()
    serializer_class = DatasetSerialiser

    permission_classes = dict(
        get_annotations=[AllowAny],  # TODO: Change to a proper level of authorisation
        get_annotations_for_image=[AllowAny],  # TODO: Change to a proper level of authorisation
        set_annotations_for_image=[AllowAny],  # TODO: Change to a proper level of authorisation
        delete_annotations_for_image=[AllowAny],  # TODO: Change to a proper level of authorisation
        **CoreDatasetViewSet.permission_classes
    )
