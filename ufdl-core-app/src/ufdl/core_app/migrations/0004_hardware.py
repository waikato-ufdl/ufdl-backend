from django.db import migrations

from ..apps import UFDLCoreAppConfig
from .hardware import iterate_hardware


def add_initial_hardware(apps, schema_editor):
    """
    Adds the standard hardware to the database.

    :param apps:            The app registry.
    :param schema_editor:   Unused.
    """
    # Get the hardware model
    hardware_model = apps.get_model(UFDLCoreAppConfig.label, "Hardware")

    # Add each standard hardware generation
    for generation, min_compute_capability, max_compute_capability in iterate_hardware():
        hardware = hardware_model(generation=generation,
                                  min_compute_capability=float(min_compute_capability),
                                  max_compute_capability=float(max_compute_capability))
        hardware.save()


class Migration(migrations.Migration):
    """
    Migration inserting the hardware presets into the database.
    """
    dependencies = [
        ('ufdl-core', '0003_standard_licences')  # Actually dependent on '0002_the_rest' but Django needs a linear
                                                 # dependency
    ]

    operations = [
        migrations.RunPython(add_initial_hardware)
    ]
