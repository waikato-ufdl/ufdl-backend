import os
from io import BytesIO
from typing import Optional
from zipfile import ZipFile

from django.db import models
from simple_django_teams.mixins import TeamOwnedModel, SoftDeleteModel, SoftDeleteQuerySet

from ..apps import APP_NAME
from ..exceptions import UnknownParameters
from .mixins import PublicModel, PublicQuerySet, AsFileModel


class DatasetQuerySet(PublicQuerySet, SoftDeleteQuerySet):
    pass


class Dataset(AsFileModel, TeamOwnedModel, PublicModel, SoftDeleteModel):
    # The name of the dataset
    name = models.CharField(max_length=200)

    # The version of the dataset
    version = models.IntegerField(default=1)

    # The project the dataset belongs to
    project = models.ForeignKey(f"{APP_NAME}.Project",
                                on_delete=models.DO_NOTHING,
                                related_name="datasets")

    # The licence type for this dataset
    licence = models.CharField(max_length=200, default="proprietary")

    # The tags applied to this dataset
    tags = models.TextField()

    objects = DatasetQuerySet.as_manager()

    file_formats = {"zip"}

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each dataset has a unique name/version pair for the project
            models.UniqueConstraint(name="unique_datasets_per_project",
                                    fields=["name", "version", "project"])
        ]

    def copy(self, creator, new_name: Optional[str] = None) -> 'Dataset':
        """
        Creates a copy of this dataset.

        :param creator:     The user creating the dataset copy.
        :param new_name:    Optional new name for the copied dataset. If absent,
                            the copy will have the same name as this dataset but
                            the version number will be incremented.
        :return:            The new dataset.
        """
        # Create the new dataset
        new_dataset = Dataset(name=new_name if new_name is not None else self.name,
                              version=1 if new_name is not None else self.version + 1,
                              project=self.project,
                              licence=self.licence,
                              tags=self.tags,
                              creator=creator)

        # Save the dataset
        new_dataset.save()

        # Add our assets to the new dataset
        from ._DataAsset import DataAsset
        for asset in self.assets.all():
            new_asset = DataAsset(filename=asset.filename,
                                  file=asset.file,
                                  dataset=new_dataset)

            new_asset.save()

        return new_dataset

    def add_file(self, filename: str, data: bytes) -> 'DataAsset':
        """
        Adds a file to the given dataset.

        :param dataset:     The dataset to add the asset to.
        :param filename:    The filename to save the asset under.
        :param data:        The asset file data.
        """
        # Validate the filename
        from ._DataAsset import DataAsset
        filename = DataAsset.validate_filename(filename)

        # Check the filename isn't already in use
        for asset in self.assets.with_filename_prefix(filename):
            if asset.filename == filename:
                raise ValueError(f"Filename {filename} is already in use")

            # N.B. directories in filenames are currently disallowed by Django)
            #      so this path should never execute (left in for good measure).
            #      See DataAsset.validate_filename.
            elif asset.filename.startswith(filename + "/"):
                raise ValueError(f"Filename {filename} is already a directory prefix")

        # Register the file with the file-system backend
        from ._File import File
        file = File.get_reference_from_backend(data)

        # Create the asset
        asset = DataAsset(filename=filename, file=file, dataset=self)
        asset.save()

        return asset

    def delete_file(self, filename: str) -> 'DataAsset':
        """
        Deletes a file from this dataset.

        :param filename:    The name of the file to delete.
        :return:            The deleted asset.
        """
        # Get the (possible) asset with the given name
        assets = self.assets.filter(filename=filename)

        # If the asset doesn't exist, it's already deleted
        if assets.count() == 0:
            return

        # Get the asset
        asset = assets.first()

        # Delete the asset
        asset.delete()

        return asset

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

    def as_zip(self) -> bytes:
        """
        Gets a zip file containing the entirety of this dataset.

        :return:    The zip file in an in-memory buffer.
        """
        # Create an in-memory buffer for the zip-file contents
        zip_buffer = BytesIO()

        # Open the buffer as a zip-file
        with ZipFile(zip_buffer, 'w') as zip_file:
            # Write each asset to the archive
            for asset in self.assets.all():
                zip_file.writestr(os.path.basename(asset.filename), asset.file.get_data())

        zip_buffer.seek(0)

        return zip_buffer.read()

    def get_owning_team(self):
        return self.project.team

    def __str__(self):
        return f"Dataset \"{self.name}\": {self.project}"
