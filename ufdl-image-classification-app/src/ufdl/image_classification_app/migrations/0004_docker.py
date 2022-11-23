from django.db import migrations

from ufdl.core_app.migrations import DataMigration
from ufdl.core_app.migrations.docker_images import get_python_docker_migration

from .docker_images import iterate_docker_images


class Migration(migrations.Migration):
    """
    Migration inserting the Docker image presets into the database.
    """
    dependencies = [
        ('ufdl_core', '0006_job_types'),
        ('ufdl_image_classification', '0003_frameworks')
    ]

    operations = [
        DataMigration(get_python_docker_migration(iterate_docker_images()))
    ]
