import importlib

from django.db import migrations

from ufdl.jobcontracts.base import UFDLJobContract

from wai.lazypip import require_module

from ..apps import UFDLCoreAppConfig
from .job_contracts import iterate_job_contracts
from ._util import DataMigration


def add_initial_job_contracts(apps, schema_editor):
    """
    Adds the initial set of job-contracts to the database.

    :param apps:            The app registry.
    :param schema_editor:   Unused.
    """
    # Get the job-contract model
    job_contract_model = apps.get_model(UFDLCoreAppConfig.label, "JobContract")

    # Add each job-contract to the database
    for name, pkg, fq_class_name in iterate_job_contracts():
        # Use lazypip to install the package and check the class
        module_name, class_name = fq_class_name.rsplit(".", 1)
        require_module(module_name, [pkg])
        cls = getattr(importlib.import_module(module_name), class_name)
        if not isinstance(cls, type) or not issubclass(cls, UFDLJobContract):
            raise Exception(f"'{fq_class_name}' is not a sub-class of {UFDLJobContract.__name__}")

        job_contract = job_contract_model(name=name, pkg=pkg, cls=fq_class_name)
        job_contract.save()


class Migration(migrations.Migration):
    """
    Migration inserting the job-contracts into the database.
    """
    dependencies = [
        ('ufdl-core', '0006_job_types')
    ]

    operations = [
        DataMigration(add_initial_job_contracts)
    ]
