import importlib

from django.db import migrations

from ufdl.jobtypes.base import UFDLType

from wai.lazypip import require_module

from ..apps import UFDLCoreAppConfig
from .job_types import iterate_job_types
from ._util import DataMigration


def add_initial_job_types(apps, schema_editor):
    """
    Adds the initial set of job-types to the database.

    :param apps:            The app registry.
    :param schema_editor:   Unused.
    """
    # Get the job-type model
    job_type_model = apps.get_model(UFDLCoreAppConfig.label, "JobType")

    # Add each job-type to the database
    for name, pkg, fq_class_name in iterate_job_types():
        # Use lazypip to install the package and check the class
        module_name, class_name = fq_class_name.rsplit(".", 1)
        require_module(module_name, [pkg])
        cls = getattr(importlib.import_module(module_name), class_name)
        if not isinstance(cls, type) or not issubclass(cls, UFDLType):
            raise Exception(f"'{fq_class_name}' is not a sub-class of {UFDLType.__name__}")

        job_type = job_type_model(name=name, pkg=pkg, cls=fq_class_name)
        job_type.save()


class Migration(migrations.Migration):
    """
    Migration inserting the job-types into the database.
    """
    dependencies = [
        ('ufdl_core', '0005_cuda')  # Actually dependent on '0002_the_rest' but Django needs a linear
                                    # dependency
    ]

    operations = [
        DataMigration(add_initial_job_types)
    ]
