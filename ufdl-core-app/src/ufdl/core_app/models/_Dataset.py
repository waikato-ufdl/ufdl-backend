from io import BytesIO
from typing import Iterator, Tuple, Optional
from zipfile import ZipFile
from tarfile import TarFile, TarInfo

from django.db import models

from simple_django_teams.mixins import TeamOwnedModel, SoftDeleteModel, SoftDeleteQuerySet

from ufdl.annotation_utils import converted_annotations_iterator

from wai.annotations.core.instance import Instance

from ..apps import UFDLCoreAppConfig
from ..exceptions import *
from ..util import QueryParameterValue
from .mixins import PublicModel, PublicQuerySet, AsFileModel, CopyableModel, FileContainerModel


class DatasetQuerySet(PublicQuerySet, SoftDeleteQuerySet):
    def with_name(self, name: str):
        """
        Filters the query-set to those data-sets with a given name.

        :param name:    The name to filter to.
        :return:        The resulting query-set.
        """
        return self.filter(name=name)

    def max_version(self) -> int:
        """
        Gets the largest version number in all of the datasets.

        :return:    The version number.
        """
        return self.aggregate(models.Max('version'))['version__max']


class Dataset(FileContainerModel, CopyableModel, AsFileModel, TeamOwnedModel, PublicModel, SoftDeleteModel):
    # The name of the dataset
    name = models.CharField(max_length=200)

    # The version of the dataset
    version = models.IntegerField(default=1, editable=False)

    # The version of the dataset that this version was copied from
    previous_version = models.IntegerField(default=-1, editable=False)

    # A description of the dataset's purpose and/or differences from previous versions
    description = models.TextField(blank=True)

    # The project the dataset belongs to
    project = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Project",
                                on_delete=models.DO_NOTHING,
                                related_name="datasets")

    # The licence type for this dataset
    licence = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Licence",
                                on_delete=models.DO_NOTHING,
                                related_name="datasets")

    # The tags applied to this dataset
    tags = models.TextField()

    # Unstructured data (use is determined by the type of dataset)
    unstructured = models.TextField()

    objects = DatasetQuerySet.as_manager()

    file_formats = {"zip", "tar.gz"}

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each dataset has a unique name/version pair for the project
            models.UniqueConstraint(name="unique_active_datasets_per_project",
                                    fields=["name", "version", "project"],
                                    condition=SoftDeleteModel.active_Q)
        ]

    def copy(self, *, creator=None, new_name=None, **kwargs) -> 'Dataset':
        """
        Creates a copy of this dataset.

        :param creator:     The user creating the dataset copy.
        :param new_name:    Optional new name for the copied dataset. If absent,
                            the copy will have the same name as this dataset but
                            the version number will be incremented.
        :return:            The new dataset.
        """
        # New name parameter must be a string
        if new_name is not None and not isinstance(new_name, str):
            raise BadName(str(new_name), "New dataset name must be a string")

        # Creator must be supplied
        if creator is None:
            raise ValueError("No creator supplied")

        # No other parameters are used
        if len(kwargs) > 0:
            raise UnknownParameters(kwargs)

        # Find the next available version number to give the copy
        new_version = 1
        if new_name is None:
            new_version = self.project.datasets.with_name(self.name).active().max_version() + 1

        # Create the new dataset
        new_dataset = type(self)(name=new_name if new_name is not None else self.name,
                                 version=new_version,
                                 previous_version=-1 if new_name is not None else self.version,
                                 description=self.description,
                                 project=self.project,
                                 licence=self.licence,
                                 tags=self.tags,
                                 creator=creator,
                                 is_public=self.is_public,
                                 unstructured=self.unstructured)

        # Save the dataset
        new_dataset.save()

        # Add our files to the new dataset
        from .files import FileReference
        for reference in self.files.all():
            new_reference = FileReference(file=reference.file, metadata=reference.metadata)
            new_reference.save()
            new_dataset.files.add(new_reference)

        return new_dataset

    def default_format(self) -> str:
        return "zip"

    def filename_without_extension(self) -> str:
        return f"{self.name}.v{self.version}"

    def as_file(self, file_format: str, **parameters: QueryParameterValue) -> bytes:
        # Extract the optional annotations arguments parameter
        annotations_args = parameters.pop("annotations_args", None)
        if isinstance(annotations_args, str):
            annotations_args = [annotations_args]

        # Create and store an annotations configuration for use in archive_file_iterator
        setattr(self, "__annotations_args", annotations_args)

        if file_format == "zip":
            # Shouldn't be any parameters
            UnknownParameters.ensure_empty(parameters)

            return self.as_zip()
        elif file_format == "tar.gz":
            # Shouldn't be any parameters
            UnknownParameters.ensure_empty(parameters)

            return self.as_tar_gz()
        else:
            raise ValueError(f"Unknown archive format '{file_format}'; options are {self.file_formats}")

    def archive_file_iterator(self) -> Iterator[Tuple[str, bytes]]:
        """
        Gets an iterator over the files to write to an
        archive when calling as_file.

        :return:    An iterator of filename, file-contents pairs.
        """
        # Retrieve the annotations arguments
        annotations_args = getattr(self, "__annotations_args")

        # Reference no longer needed after this method returns
        delattr(self, "__annotations_args")

        # If no annotations arguments supplied, just return the files
        if annotations_args is None:
            return ((file_reference.file.filename, file_reference.file.get_data())
                    for file_reference in self.files.all())

        # Convert our annotations
        annotations_file_iterator = converted_annotations_iterator(
            self.get_annotations_iterator(),
            *annotations_args
        )

        # Converted annotations files are supplied as streams, but we are required
        # to return the file contents as bytes, so do a complete read
        return ((filename, file.read()) for filename, file in annotations_file_iterator)

    def get_annotations_iterator(self) -> Optional[Iterator[Instance]]:
        """
        Gets an iterator over the instances in this dataset in
        the domain format used by wai.annotations.

        :return:    The instance iterator
        """
        # Returns None by default, sub-types should override this
        return None

    def as_zip(self) -> bytes:
        """
        Gets a zip file containing the entirety of this data-set.

        :return:    The zip file in an in-memory buffer.
        """
        # Create an in-memory buffer for the zip-file contents
        zip_buffer = BytesIO()

        # Open the buffer as a zip-file
        with ZipFile(zip_buffer, 'w') as zip_file:
            # Write each file to the archive
            for filename, contents in self.archive_file_iterator():
                zip_file.writestr(filename, contents)

        # Reset the buffer to the beginning for reading
        zip_buffer.seek(0)

        return zip_buffer.read()

    def as_tar_gz(self) -> bytes:
        """
        Gets a tar.gz file containing the entirety of this data-set.

        :return:    The tar.gz file in an in-memory buffer.
        """
        # Create an in-memory buffer for the file contents
        tar_buffer = BytesIO()

        # Open the buffer as a zip-file
        with TarFile.open(fileobj=tar_buffer, mode='w:gz') as tar_file:
            # Write each file to the archive
            for filename, contents in self.archive_file_iterator():
                info = TarInfo(filename)
                info.size = len(contents)
                tar_file.addfile(info, BytesIO(contents))

        # Reset the buffer to the beginning for reading
        tar_buffer.seek(0)

        return tar_buffer.read()

    def get_owning_team(self):
        return self.project.team

    def __str__(self):
        return f"Dataset \"{self.name}\": {self.project}"
