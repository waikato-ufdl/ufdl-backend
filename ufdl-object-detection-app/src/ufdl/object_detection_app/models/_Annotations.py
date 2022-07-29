from typing import Any, Callable, List, Optional, Set, Type, TypeVar, Union

from django.db import models

from ufdl.core_app.models.files import FileReference

from ufdl.json.object_detection import Image, Video, AnnotationsFile, File

from ..models import Annotation

FileType = TypeVar('FileType', bound=File)


class AnnotationsQuerySet(models.QuerySet):
    """
    Represents a query-set of the annotations for images in an
    object-detection data-set.
    """
    @property
    def json(self) -> AnnotationsFile:
        """
        Formats this set of annotations as a JSON annotations file.
        """
        return AnnotationsFile(
            **{
                annotations.filename: annotations.json
                for annotations in self.all()
            }
        )

    def for_file(self, file: Union[str, FileReference]) -> 'AnnotationsQuerySet':
        """
        Filters the query-set to those annotations that are for a particular file.

        :param file:
                    The name of the file to filter for.
        :return:
                    The filtered query-set.
        """
        if isinstance(file, str):
            return self.filter(file__file__name__filename=file)

        return self.filter(file=file)


class Annotations(models.Model):
    """
    Represents the annotations for a single image in an object-detection
    data-set.
    """
    # The file the annotations belong to
    file = models.OneToOneField(
        FileReference,
        on_delete=models.DO_NOTHING,
        related_name="+"
    )

    # The format of the image/video
    format = models.CharField(max_length=4, null=True, default=None)

    # The width of the image/video, in pixels
    width = models.IntegerField(null=True, default=None)

    # The height of the image/video, in pixels
    height = models.IntegerField(null=True, default=None)

    # The length of the video, None for images
    video_length = models.FloatField(null=True, default=None)

    objects = AnnotationsQuerySet.as_manager()

    @property
    def filename(self) -> str:
        """
        The name of the file to which these annotations belong.
        """
        return self.file.filename

    @property
    def is_image(self) -> bool:
        """
        Whether these annotations are for an image.
        """
        return self.video_length is None

    @property
    def is_video(self) -> bool:
        """
        Whether these annotations are for a video.
        """
        return not self.is_image

    @property
    def json(self) -> Union[Image, Video]:
        """
        Creates an Image/Video JSON object from this set of annotations.
        """
        if self.is_image:
            return self._to_json_image()
        else:
            return self._to_json_video()

    @property
    def labels(self) -> Set[str]:
        """
        The set of labels in these annotations.
        """
        return set(
            annotation.label
            for annotation in self.annotations.all()
        )

    def _to_json_image(self) -> Image:
        """
        TODO
        :return:
        """
        return self.to_file(Image, lambda annotation: annotation.json_image)

    def _to_json_video(self) -> Video:
        """
        TODO
        :return:
        """
        return self.to_file(Video, lambda annotation: annotation.json_video)

    def to_file(
            self,
            cls: Type[FileType],
            convert_annotations: Optional[Callable[[Annotation], Any]]
    ) -> FileType:
        """
        TODO
        :return:
        """
        kwargs = {}

        # Parse the individual fields into JSON
        format = self.format
        if format is not None:
            kwargs['format'] = format
        dimensions = [self.width, self.height]
        if dimensions[0] is not None and dimensions[1] is not None:
            kwargs['dimensions'] = dimensions
        length = self.video_length
        if length is not None:
            kwargs['length'] = length
        if convert_annotations is not None:
            kwargs['annotations'] = list(
                map(
                    convert_annotations,
                    self.annotations.all()
                )
            )

        return cls(**kwargs)
