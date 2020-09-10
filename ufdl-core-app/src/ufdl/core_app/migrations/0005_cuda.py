from django.db import migrations

from ..apps import UFDLCoreAppConfig
from .cuda import iterate_cuda
from ._util import DataMigration


def add_initial_cuda(apps, schema_editor):
    """
    Adds the standard CUDA versions to the database.

    :param apps:            The app registry.
    :param schema_editor:   Unused.
    """
    # Get the CUDA version model
    cuda_model = apps.get_model(UFDLCoreAppConfig.label, "CUDAVersion")

    # Add each CUDA version to the database
    for version, full_version, min_driver_version in iterate_cuda():
        cuda = cuda_model(version=version, full_version=full_version, min_driver_version=min_driver_version)
        cuda.save()


class Migration(migrations.Migration):
    """
    Migration inserting the CUDA presets into the database.
    """
    dependencies = [
        ('ufdl-core', '0004_hardware')  # Actually dependent on '0002_the_rest' but Django needs a linear
                                        # dependency
    ]

    operations = [
        DataMigration(add_initial_cuda)
    ]
