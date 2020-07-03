from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.core_app.exceptions import *
from ufdl.core_app.views.mixins import RoutedViewSet

from ufdl.json.object_detection import AnnotationsModSpec

from ...models import ObjectDetectionDataset


class AnnotationsViewSet(RoutedViewSet):
    """
    Mixin for view-sets which allow the adding/removing of annotations from files.
    """
    # The keyword used to specify when the view-set is in annotations mode
    MODE_KEYWORD: str = "annotations"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/annotations{trailing_slash}$',
                mapping={'get': 'get_annotations'},
                name='{basename}-annotations',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AnnotationsViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/annotations/(?P<fn>.+){trailing_slash}$',
                mapping={'get': 'get_annotations_for_image',
                         'post': 'set_annotations_for_image',
                         'delete': 'delete_annotations_for_image'},
                name='{basename}-annotations-for-image',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AnnotationsViewSet.MODE_KEYWORD}
            )
        ]

    def get_annotations(self, request: Request, pk=None):
        """
        Gets the annotations of a data-set.

        :param request:     The request.
        :param pk:          The primary key of the data-set being accessed.
        :return:            The response containing the annotations.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Return the annotations
        return Response(dataset.get_annotations().to_raw_json())

    def get_annotations_for_image(self, request: Request, pk=None, fn=None):
        """
        Gets the annotations for a particular image in a data-set.

        :param request:     The request.
        :param pk:          The primary key of the data-set being accessed.
        :param fn:          The filename of the image.
        :return:            The response containing the annotations.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Get the annotations
        annotations = dataset.get_annotations_for_image(fn)

        # Return the annotations
        return Response(list(annotation.to_raw_json() for annotation in annotations))

    def set_annotations_for_image(self, request: Request, pk=None, fn=None):
        """
        Sets the annotations for a particular image in a data-set.

        :param request:     The request.
        :param pk:          The primary key of the data-set being accessed.
        :param fn:          The filename of the image.
        :return:            The response.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Get the annotations from the request
        annotations = JSONParseFailure.attempt(dict(request.data), AnnotationsModSpec).annotations

        # Set the annotations
        dataset.set_annotations_for_image(fn, annotations)

        # Return an empty response
        return Response({})

    def delete_annotations_for_image(self, request: Request, pk=None, fn=None):
        """
        Deletes the annotations for a particular image in a data-set.

        :param request:     The request.
        :param pk:          The primary key of the data-set being accessed.
        :param fn:          The filename of the image.
        :return:            The response.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Set the annotations
        dataset.set_annotations_for_image(fn, [])

        # Return an empty response
        return Response({})
