import os

from django.db import models
from simple_django_teams.mixins import TeamOwnedModel

from ..apps import APP_NAME


class DataAssetQuerySet(models.QuerySet):
    def with_filename_prefix(self, prefix: str):
        """
        Filters the query-set to those assets whose file-names
        begin with a given prefix.

        :param prefix:  The prefix to search for.
        :return:        The filtered query-set.
        """
        return self.filter(filename__startswith=prefix)


class DataAsset(TeamOwnedModel):
    """
    An asset of a dataset on disk. Data assets should not
    be modified (to do so delete the asset and then add a
    modified version).
    """
    # The logical filename of the asset
    filename = models.CharField(max_length=200,
                                editable=False)

    # The file reference of the asset with the file-system backend
    file = models.ForeignKey(f"{APP_NAME}.File",
                             on_delete=models.DO_NOTHING,
                             related_name="assets",
                             editable=False)

    # The dataset the asset belongs to
    dataset = models.ForeignKey(f"{APP_NAME}.Dataset",
                                on_delete=models.DO_NOTHING,
                                related_name="assets",
                                editable=False)

    objects = DataAssetQuerySet.as_manager()

    class Meta(TeamOwnedModel.Meta):
        constraints = [
            # Ensure that each dataset has a unique name/version pair for the project
            models.UniqueConstraint(name="unique_data_asset_names",
                                    fields=["filename", "dataset"])
        ]

    @classmethod
    def validate_filename(cls, original_filename: str) -> str:
        """
        Validates the a given filename is a valid filename
        (syntactically only). Returns the regularised version
        of the filename.

        N.B. This allows for logical filenames to include relative
        directory paths (so long as they don't go outside the top-
        level directory), but this is never used as Django itself
        removes directory paths from the uploaded filenames.

        :param original_filename:   The filename to validate.
        :return:                    The regularised filename.
        """
        # Collapse redundant slashes/dots
        filename = os.path.normpath(original_filename)

        # Remove any initial slashes
        while filename.startswith(os.sep):
            filename = filename[1:]

        # Can't end in a slash
        if filename.endswith(os.sep):
            raise ValueError(f"Filename {original_filename} specifies a directory (ends in {os.sep})")

        # Can't specify a relative directory outside the top-level
        if filename.startswith(".."):
            raise ValueError(f"Filename {original_filename} cannot extend beyond top-level directory (starts with ..)")

        return filename

    def get_owning_team(self):
        return self.dataset.project.team

    def __str__(self):
        return f"Data Asset \"{self.filename}\": {self.dataset}"
