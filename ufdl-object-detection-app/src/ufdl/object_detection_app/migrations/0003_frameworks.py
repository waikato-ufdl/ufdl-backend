from django.db import migrations

from ufdl.core_app.migrations import DataMigration
from ufdl.core_app.migrations.framework import get_python_docker_migration

from .frameworks import iterate_frameworks


class Migration(migrations.Migration):
    """
    Migration inserting the framework presets into the database.
    """
    dependencies = [
        ('ufdl_core', '0006_job_types'),
        ('ufdl_object_detection', '0002_add_data_domain')
    ]

    operations = [
        DataMigration(get_python_docker_migration(iterate_frameworks()))
    ]
