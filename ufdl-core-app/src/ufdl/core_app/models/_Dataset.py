from io import BytesIO
from zipfile import ZipFile
from tarfile import TarFile, TarInfo

from django.db import models
from simple_django_teams.mixins import TeamOwnedModel, SoftDeleteModel, SoftDeleteQuerySet

from ..apps import UFDLCoreAppConfig
from ..exceptions import UnknownParameters, BadName
from .mixins import PublicModel, PublicQuerySet, AsFileModel, CopyableModel, FileContainerModel


class DatasetQuerySet(PublicQuerySet, SoftDeleteQuerySet):
    pass


class Dataset(FileContainerModel, CopyableModel, AsFileModel, TeamOwnedModel, PublicModel, SoftDeleteModel):
    # The name of the dataset
    name = models.CharField(max_length=200)

    # The version of the dataset
    version = models.IntegerField(default=1)

    # The project the dataset belongs to
    project = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Project",
                                on_delete=models.DO_NOTHING,
                                related_name="datasets")

    # The licence type for this dataset
    licence = models.CharField(max_length=200, default="proprietary")

    # The tags applied to this dataset
    tags = models.TextField()

    objects = DatasetQuerySet.as_manager()

    file_formats = {"zip", "tar.gz"}

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each dataset has a unique name/version pair for the project
            models.UniqueConstraint(name="unique_datasets_per_project",
                                    fields=["name", "version", "project"])
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

        # Create the new dataset
        new_dataset = Dataset(name=new_name if new_name is not None else self.name,
                              version=1 if new_name is not None else self.version + 1,
                              project=self.project,
                              licence=self.licence,
                              tags=self.tags,
                              creator=creator)

        # Save the dataset
        new_dataset.save()

        # Add our files to the new dataset
        for file in self.files.all():
            new_dataset.files.add(file)

        return new_dataset

    def default_format(self) -> str:
        return "zip"

    def filename_without_extension(self) -> str:
        return f"{self.name}.v{self.version}"

    def as_file(self, file_format: str, **parameters) -> bytes:
        if file_format == "zip":
            # Shouldn't be any parameters
            if len(parameters) > 0:
                raise UnknownParameters(parameters)
            return self.as_zip()
        elif file_format == "tar.gz":
            # Shouldn't be any parameters
            if len(parameters) > 0:
                raise UnknownParameters(parameters)
            return self.as_tar_gz()

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
            for file in self.files.all():
                zip_file.writestr(file.filename, file.get_data())

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
            for file in self.files.all():
                file_data = file.get_data()
                info = TarInfo(file.filename)
                info.size = len(file_data)
                tar_file.addfile(info, BytesIO(file_data))

        # Reset the buffer to the beginning for reading
        tar_buffer.seek(0)

        return tar_buffer.read()

    def get_owning_team(self):
        return self.project.team

    def __str__(self):
        return f"Dataset \"{self.name}\": {self.project}"
