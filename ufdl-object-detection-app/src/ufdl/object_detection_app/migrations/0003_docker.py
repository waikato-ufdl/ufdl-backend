from django.db import migrations

from ufdl.core_app.migrations.docker_images import get_python_docker_migration

from .docker_images import iterate_docker_images


class Migration(migrations.Migration):
    """
    Migration inserting the Docker image presets into the database.
    """
    dependencies = [
        ('ufdl-core', '0007_job_types'),
        ('ufdl-object-detection', '0002_add_data_domain')
    ]

    operations = [
        migrations.RunPython(get_python_docker_migration(iterate_docker_images()))
    ]
