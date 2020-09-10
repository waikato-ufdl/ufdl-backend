from django.db import migrations

from ..apps import UFDLCoreAppConfig
from .framework import iterate_frameworks
from ._util import DataMigration


def add_initial_frameworks(apps, schema_editor):
    """
    Adds the standard frameworks to the database.

    :param apps:            The app registry.
    :param schema_editor:   Unused.
    """
    # Get the Framework model
    framework_model = apps.get_model(UFDLCoreAppConfig.label, "Framework")

    # Add each framework version to the database
    for name, version in iterate_frameworks():
        framework = framework_model(name=name, version=version)
        framework.save()


class Migration(migrations.Migration):
    """
    Migration inserting the framework presets into the database.
    """
    dependencies = [
        ('ufdl-core', '0005_cuda')  # Actually dependent on '0002_the_rest' but Django needs a linear
                                    # dependency
    ]

    operations = [
        DataMigration(add_initial_frameworks)
    ]
