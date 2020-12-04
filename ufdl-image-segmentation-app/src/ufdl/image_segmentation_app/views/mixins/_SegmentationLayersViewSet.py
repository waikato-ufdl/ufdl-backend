from typing import List

from rest_framework import routers
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.core_app.exceptions import MissingParameter, BadArgumentValue, BadArgumentType
from ufdl.core_app.renderers import BinaryFileRenderer
from ufdl.core_app.views.mixins import RoutedViewSet

from ...models import ImageSegmentationDataset


class SegmentationLayersViewSet(RoutedViewSet):
    """
    Mixin for view-sets which allow the adding/removing of
    segmentation layers/labels from files.
    """
    # The keyword used to specify when the view-set is in layers mode
    LAYERS_MODE_KEYWORD: str = "segmentation-layers"

    # The keyword used to specify when the view-set is in labels mode
    LABELS_MODE_KEYWORD: str = "segmentation-labels"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/layers/(?P<fn>.*)/(?P<lbl>[^/]+){trailing_slash}$',
                mapping={'get': 'get_layer',
                         'post': 'set_layer'},
                name='{basename}-segmentation-layers',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: SegmentationLayersViewSet.LAYERS_MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/labels{trailing_slash}$',
                mapping={'get': 'get_labels',
                         'post': 'set_labels'},
                name='{basename}-segmentation-labels',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: SegmentationLayersViewSet.LABELS_MODE_KEYWORD}
            )
        ]

    def get_parsers(self):
        # If not posting a file, return the standard parsers
        if self.mode != SegmentationLayersViewSet.LAYERS_MODE_KEYWORD or self.request.method != 'POST':
            return super().get_parsers()

        return [FileUploadParser()]

    def get_renderers(self):
        # If not getting a file, return the standard renderers
        if self.mode != SegmentationLayersViewSet.LAYERS_MODE_KEYWORD or self.request.method != 'GET':
            return super().get_renderers()

        return [BinaryFileRenderer()]

    def get_layer(self, request: Request, pk=None, fn=None, lbl=None):
        """
        Gets a layer image from this data-set.

        :param request:
                    The request.
        :param pk:
                    The primary key of the data-set being accessed.
        :param fn:
                    The data-file the layer is for.
        :param lbl:
                    The label the layer describes.
        :return:
                    The response containing the layer image.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ImageSegmentationDataset)


        # Get the layer's image data
        layer_data = dataset.get_layer(fn, lbl)

        # If there is no layer data for this label, return an empty data stream
        if layer_data is None:
            layer_data = b''

        # Return the categories
        return Response(layer_data)

    def set_layer(self, request: Request, pk=None, fn=None, lbl=None):
        """
        Sets a layer image from this data-set.

        :param request:
                    The request containing the file data.
        :param pk:
                    The primary key of the data-set being accessed.
        :param fn:
                    The data-file the layer is for.
        :param lbl:
                    The label the layer describes.
        :return:
                    The response containing the label.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ImageSegmentationDataset)

        # Buffer the file data
        file_data = request.data['file'].file.read()

        # Set the layer for the data-set
        dataset.set_layer(fn, lbl, file_data)

        # Return the categories
        return Response(lbl)

    def get_labels(self, request: Request, pk=None):
        """
        Gets the labels for this data-set.

        :param request:
                    The request.
        :param pk:
                    The primary key of the data-set being accessed.
        :return:
                    The response containing the labels.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ImageSegmentationDataset)

        # Return the categories
        return Response(dataset.get_labels())

    def set_labels(self, request: Request, pk=None):
        """
        Sets the labels for this data-set.

        :param request:
                    The request containing the labels.
        :param pk:
                    The primary key of the data-set being accessed.
        :return:
                    The response containing the labels.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ImageSegmentationDataset)

        # Get the labels from the request
        data = dict(request.data)
        if 'labels' not in data:
            raise MissingParameter('labels')
        labels = data['labels']

        # Labels must be a list
        if not isinstance(labels, list):
            raise BadArgumentType("set_labels", "labels", "list", labels)

        # Label elements must be strings
        for index, label in enumerate(labels):
            if not isinstance(label, str):
                raise BadArgumentType("set_labels", f"labels[{index}]", "str", label)

        # Labels must be unique
        if len(labels) != len(set(labels)):
            raise BadArgumentValue(
                "set_labels",
                "labels",
                str(labels),
                reason="Duplicate labels"
            )

        # Set the labels of the dataset
        dataset.set_labels(labels)

        # Return the categories
        return Response(labels)
