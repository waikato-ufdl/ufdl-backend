from django.db import migrations

from ..apps import UFDLCoreAppConfig
from .job_types import iterate_job_types


def add_initial_job_types(apps, schema_editor):
    """
    Adds the initial set of job-types to the database.

    :param apps:            The app registry.
    :param schema_editor:   Unused.
    """
    # Get the job-type model
    job_type_model = apps.get_model(UFDLCoreAppConfig.label, "JobType")

    # Add each job-type to the database
    for name, in iterate_job_types():
        job_type = job_type_model(name=name)
        job_type.save()


class Migration(migrations.Migration):
    """
    Migration inserting the job-types into the database.
    """
    dependencies = [
        ('ufdl-core', '0007_docker')  # Actually dependent on '0002_the_rest' but Django needs a linear
                                      # dependency
    ]

    operations = [
        migrations.RunPython(add_initial_job_types)
    ]
