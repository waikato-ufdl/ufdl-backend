from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.core_app.exceptions import *
from ufdl.core_app.views.mixins import RoutedViewSet

from ufdl.json.object_detection import FileType, AnnotationsFile, ImageAnnotation, VideoAnnotation

from wai.json.object import Absent

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
                url=r'^{prefix}/{lookup}/labels{trailing_slash}$',
                mapping={
                    'get': 'get_labels',
                    'post': 'add_labels'
                },
                name='{basename}-labels',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AnnotationsViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/labels/(?P<lbl>.+){trailing_slash}$',
                mapping={
                    'delete': 'delete_label'
                },
                name='{basename}-labels-delete',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AnnotationsViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/prefixes{trailing_slash}$',
                mapping={
                    'get': 'get_prefixes',
                    'post': 'add_prefixes'
                },
                name='{basename}-prefixes',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AnnotationsViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/prefixes/(?P<pfx>.+){trailing_slash}$',
                mapping={
                    'delete': 'delete_prefix'
                },
                name='{basename}-prefixes-delete',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AnnotationsViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/file-type/(?P<fn>.+)$',
                mapping={
                    'get': 'get_file_type',
                    'post': 'set_file_type'
                },
                name='{basename}-file-types',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AnnotationsViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/file-types{trailing_slash}$',
                mapping={
                    'get': 'get_file_types'
                },
                name='{basename}-file-types-bulk',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AnnotationsViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/annotations{trailing_slash}$',
                mapping={
                    'get': 'get_annotations',
                    'post': 'set_annotations',
                    'delete': 'clear_annotations'
                },
                name='{basename}-annotations',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AnnotationsViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/annotations/(?P<fn>.+)$',
                mapping={'get': 'get_annotations_for_file',
                         'post': 'set_annotations_for_file',
                         'patch': 'add_annotations_to_file',
                         'delete': 'delete_annotations_for_file'},
                name='{basename}-annotations-for-file',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AnnotationsViewSet.MODE_KEYWORD}
            ),
        ]

    def get_labels(self, request: Request, pk=None):
        """
        Gets the labels of a data-set.

        :param request:     The request.
        :param pk:          The primary key of the data-set being accessed.
        :return:            The response containing the labels.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Get the labels from the data-set
        labels = list(dataset.get_labels())

        # Sort the labels
        labels.sort()

        # Return the labels
        return Response(labels)

    def add_labels(self, request: Request, pk=None):
        """
        Adds new labels to the dataset.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Get the labels from the request
        labels = request.data

        # Make sure all labels are strings
        if (
                not isinstance(labels, (tuple, list)) or
                not all(isinstance(label, str) for label in labels)
        ):
            raise BadArgumentType(
                "add_labels",
                "data",
                "List[str]",
                labels
            )

        # Add the labels
        for label in labels:
            dataset.add_label(label)

        # Return an empty response
        return Response({})

    def delete_label(self, request: Request, pk=None, lbl=None):
        """
        Removes a label from the dataset.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Delete the labels
        dataset.remove_label(lbl)

        # Return an empty response
        return Response({})

    def get_prefixes(self, request: Request, pk=None):
        """
        Gets the prefixes of a data-set.

        :param request:
                    The request.
        :param pk:
                    The primary key of the data-set being accessed.
        :return:
                    The response containing the prefixes.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Get the prefixes from the data-set
        prefixes = list(dataset.get_prefixes())

        # Sort the prefixes
        prefixes.sort()

        # Return the prefixes
        return Response(prefixes)

    def add_prefixes(self, request: Request, pk=None):
        """
        Adds new prefixes to the dataset.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Get the prefixes from the request
        prefixes = request.data

        # Make sure all prefixes are strings
        if (
                not isinstance(prefixes, (tuple, list)) or
                not all(isinstance(prefix, str) for prefix in prefixes)
        ):
            raise BadArgumentType(
                "add_prefixes",
                "data",
                "List[str]",
                prefixes
            )

        # Add the prefixes
        for prefix in prefixes:
            dataset.add_prefix(prefix)

        # Return an empty response
        return Response({})

    def delete_prefix(self, request: Request, pk=None, pfx=None):
        """
        Removes a prefix from the dataset.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Delete the prefix
        dataset.remove_label(pfx)

        # Return an empty response
        return Response({})

    def get_file_type(self, request: Request, pk=None, fn=None):
        """
        Sets the file-type of a file in the dataset.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Get the file-type for the given file
        annotations = dataset.get_file_type(fn)

        # Return an empty response
        return Response(annotations.to_file(FileType, None).to_raw_json())

    def set_file_type(self, request: Request, pk=None, fn=None):
        """
        Sets the file-type of a file in the dataset.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Parse the body
        file_type = JSONParseFailure.attempt(
            dict(request.data),
            FileType
        )

        # Set the file-type
        dataset.set_file_type(
            fn,
            None if file_type.format is Absent else file_type.format,
            file_type.width,
            file_type.height,
            None if file_type.length is Absent else file_type.length
        )

        # Return an empty response
        return Response({})

    def get_file_types(self, request: Request, pk=None):
        """
        Sets the file-type of a file in the dataset.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Return an empty response
        return Response({
            annotations.filename: annotations.to_file(FileType, None).to_raw_json()
            for annotations in dataset.annotations.all()
        })

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
        return Response(dataset.get_annotations().to_raw_json(validate=False))

    def set_annotations(self, request: Request, pk=None):
        """
        Sets the annotations for the dataset.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Parse the body
        annotations = JSONParseFailure.attempt(
            dict(request.data),
            AnnotationsFile
        )

        dataset.set_annotations(annotations)

        return Response({})

    def clear_annotations(self, request: Request, pk=None):
        """
        Clears all annotations from this dataset.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        dataset.clear_annotations()

        return Response({})

    def get_annotations_for_file(self, request: Request, pk=None, fn=None):
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
        annotations = dataset.get_annotations_for_file(fn)

        # Return the annotations
        return Response(annotations)

    def set_annotations_for_file(self, request: Request, pk=None, fn=None):
        """
        Sets the annotations for a particular image in a data-set.

        :param request:     The request.
        :param pk:          The primary key of the data-set being accessed.
        :param fn:          The filename of the image.
        :return:            The response.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Make sure the JSON is a list/tuple
        if not isinstance(request.data, (tuple, list)):
            raise BadArgumentType(
                "set_annotations_for_file",
                "data",
                "List/Tuple",
                request.data
            )

        # Ensure the annotations are valid
        annotations = [
            JSONParseFailure.attempt_multi(raw_json, ImageAnnotation, VideoAnnotation)
            for raw_json in request.data
        ]

        # Set the annotations
        dataset.set_annotations_for_file(fn, annotations)

        # Return an empty response
        return Response({})

    def add_annotations_to_file(self, request: Request, pk=None, fn=None):
        """
        Adds annotations to a particular file in a data-set.

        :param request:     The request.
        :param pk:          The primary key of the data-set being accessed.
        :param fn:          The filename of the file.
        :return:            The response.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ObjectDetectionDataset)

        # Make sure the JSON is a list/tuple
        if not isinstance(request.data, (tuple, list)):
            raise BadArgumentType(
                "add_annotations_to_file",
                "data",
                "List/Tuple",
                request.data
            )

        # Ensure the annotations are valid
        annotations = [
            JSONParseFailure.attempt_multi(raw_json, ImageAnnotation, VideoAnnotation)
            for raw_json in request.data
        ]

        # Set the annotations
        for annotation in annotations:
            dataset.add_annotation_to_file(fn, annotation)

        # Return an empty response
        return Response({})

    def delete_annotations_for_file(self, request: Request, pk=None, fn=None):
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
        dataset.clear_annotations_for_file(fn)

        # Return an empty response
        return Response({})
