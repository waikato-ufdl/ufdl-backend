from io import BytesIO
from typing import Iterator, Tuple, Optional
from zipfile import ZipFile
from tarfile import TarFile, TarInfo

from django.db import models

from simple_django_teams.mixins import TeamOwnedModel, SoftDeleteModel, SoftDeleteQuerySet
from simple_django_teams.models import Team

from ufdl.annotation_utils import converted_annotations_iterator

from wai.annotations.core.domain import Instance

from ..apps import UFDLCoreAppConfig
from ..exceptions import *
from ..util import QueryParameterValue, for_user, format_suffix, max_value
from .mixins import (
    PublicModel, PublicQuerySet, AsFileModel, CopyableModel, FileContainerModel, UserRestrictedQuerySet,
    MergableModel
)


class DatasetQuerySet(UserRestrictedQuerySet, PublicQuerySet, SoftDeleteQuerySet):
    def with_name(self, name: str):
        """
        Filters the query-set to those data-sets with a given name.

        :param name:    The name to filter to.
        :return:        The resulting query-set.
        """
        return self.filter(name=name)

    def with_version(self, version: int):
        """
        Filters the query-set to those data-sets with a given version.

        :param version:     The version to filter to.
        :return:            The resulting query-set.
        """
        return self.filter(version=version)

    def max_version(self) -> int:
        """
        Gets the largest version number in all of the datasets.

        :return:    The version number.
        """
        return max_value(self, "version", 0)

    def for_user(self, user):
        # Users can see all public datasets and any datasets belonging to teams
        # the user is part of
        return self.filter(
            models.Q(Dataset.public_Q) |
            models.Q(project__team__in=for_user(Team.objects, user))
        )


class Dataset(MergableModel, FileContainerModel, CopyableModel, AsFileModel, TeamOwnedModel, PublicModel, SoftDeleteModel):
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

    # The data-domain the dataset is in
    domain = models.ForeignKey(f"{UFDLCoreAppConfig.label}.DataDomain",
                               on_delete=models.DO_NOTHING,
                               related_name="datasets",
                               null=True,
                               editable=False)

    objects = DatasetQuerySet.as_manager()

    file_formats = {"zip", "tar.gz"}

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each dataset has a unique name/version pair for the project
            models.UniqueConstraint(name="unique_active_datasets_per_project",
                                    fields=["name", "version", "project"],
                                    condition=SoftDeleteModel.active_Q)
        ]

    @property
    def domain_specific(self):
        """
        Converts this data-set instance into the domain-specific model.

        :return:    The domain-specific representation of this data-set.
        """
        # Already domain-specific, return self
        if not type(self) is Dataset:
            return self

        # Not a domain-specific data-set, return self
        if self.domain is None:
            return self

        # Format the domain prefix
        prefix: str = self.domain.description
        prefix = prefix.lower().replace(" ", "")

        return getattr(self, f"{prefix}dataset")

    @classmethod
    def domain_code(cls) -> Optional[str]:
        """
        Gets the domain-code for this type of data-set.
        """
        return None

    def merge(self, other) -> 'Dataset':
        # Make sure the other object is the same kind of data-set as we are.
        if not type(self) is type(other):
            raise Exception(f"Expected to merge with another {type(self).__name__} but "
                            f"received a {type(other).__name__} instead")

        # Gather a mapping from source file to new file
        new_files = []

        # Add the other data-set's file to this one
        for other_file in other.files.all():
            # Get the filename of the file
            filename = other_file.filename

            # See if we have a file by the same name
            self_file = self.get_file_reference(filename)

            # If we do...
            if self_file is not None:
                # If it has different contents, copy it with an extended filename
                if not self_file.has_same_contents_as(other_file):
                    # Search for an unused filename
                    extension = 1
                    new_filename = format_suffix(filename, extension)
                    while self.has_file(new_filename):
                        extension += 1
                        new_filename = format_suffix(filename, extension)

                    # Create a copy with the new filename
                    new_file = other_file.copy(new_name=new_filename)

                # If it has the same contents and name, just keep the current file
                else:
                    new_file = self_file

            # If we don't have a file by that name, copy the source file
            else:
                new_file = other_file.copy()

            # Add the new file if we made a copy of the original
            if new_file is not self_file:
                self.files.add(new_file)

            new_files.append((other_file, new_file))

        # Merge any annotations for the files
        self.merge_annotations(other, new_files)

    def merge_annotations(self, other, files):
        """
        Merges the annotations for a particular file in another
        data-set into this one.

        :param other:   The other data-set.
        :param files:   A list of pairs of (source_file, target_file).
        """
        # Default implementation is to do nothing
        pass

    def clear(self):
        """
        Clears all annotations and meta-data from this data-set.
        """
        # Remove all meta-data
        for file in self.files.all():
            file.metadata = ""
            file.save()

        # Remove annotations
        self.clear_annotations()

    def clear_annotations(self):
        """
        Clears all annotations from this data-set.
        """
        # Default implementation is to do nothing
        pass

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
        else:
            # Check that the new name is not already in use
            if self.project.datasets.with_name(new_name).with_version(1).active().exists():
                raise BadName(new_name, "New dataset name is already taken")

        # Create the new dataset
        new_dataset = type(self)(name=new_name if new_name is not None else self.name,
                                 version=new_version,
                                 previous_version=-1 if new_name is not None else self.version,
                                 description=self.description,
                                 project=self.project,
                                 licence=self.licence,
                                 tags=self.tags,
                                 creator=creator,
                                 is_public=self.is_public)

        # Save the dataset
        new_dataset.save()

        # Create a list of files to merge annotations for
        merge_files = []

        # Add our files to the new dataset
        for reference in self.files.all():
            new_file = reference.copy()
            merge_files.append((reference, new_file))
            new_dataset.files.add(new_file)

        # Copy the annotations for this data-set
        new_dataset.merge_annotations(self, merge_files)

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
        if annotations_args is None or type(self) is Dataset:
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
