from typing import Optional

from django.db import models
from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet

from ...apps import UFDLCoreAppConfig
from ...util import QueryParameterValue
from ..mixins import AsFileModel, SetFileModel


class ModelQuerySet(SoftDeleteQuerySet):
    """
    A query-set over deep-learning models.
    """
    pass


class Model(SetFileModel, AsFileModel, SoftDeleteModel):
    """
    A deep-learning model.

    TODO: Who owns a model? A team? A project? The server as a whole?
    """
    # The framework the model works with
    framework = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Framework",
                                  on_delete=models.DO_NOTHING,
                                  related_name="models")

    # The domain the model operates in
    domain = models.ForeignKey(f"{UFDLCoreAppConfig.label}.DataDomain",
                               on_delete=models.DO_NOTHING,
                               related_name="models")

    # The licence type for this model
    licence = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Licence",
                                on_delete=models.DO_NOTHING,
                                related_name="models")

    # The data of the model
    data = models.ForeignKey(f"{UFDLCoreAppConfig.label}.File",
                             on_delete=models.DO_NOTHING,
                             related_name="+",
                             null=True,
                             default=None)

    @property
    def has_data(self) -> bool:
        return self.data is not None

    objects = ModelQuerySet.as_manager()

    def supports_file_format(self, file_format: str):
        return file_format == 'data'

    def default_format(self) -> str:
        return 'data'

    def filename_without_extension(self) -> str:
        return 'model'

    def as_file(self, file_format: str, **parameters: QueryParameterValue) -> bytes:
        return self.data.get_data() if self.data is not None else b''

    def set_file(self, data: Optional[bytes]):
        # Local import to avoid dependency cycles
        from ..files import File

        # Get the current file
        current = self.data

        # If the file is present, delete it
        if current is not None:
            current.delete()

        # Set the new file to the given data
        self.data = File.get_reference_from_backend(data) if data is not None else None

        # Save
        self.save(update_fields="data")
