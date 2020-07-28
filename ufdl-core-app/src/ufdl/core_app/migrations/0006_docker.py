from decimal import Decimal

from django.db import migrations

from ..apps import UFDLCoreAppConfig
from .docker_images import iterate_docker_images


def add_initial_docker_images(apps, schema_editor):
    """
    Adds the standard Docker images to the database.

    :param apps:            The app registry.
    :param schema_editor:   Unused.
    """
    # Get the required models
    hardware_model = apps.get_model(UFDLCoreAppConfig.label, "Hardware")
    cuda_model = apps.get_model(UFDLCoreAppConfig.label, "CUDAVersion")
    docker_image_model = apps.get_model(UFDLCoreAppConfig.label, "DockerImage")

    # Add each Docker image to the database
    for (name, version, url, registry_url, registry_username, registry_password, cuda_version,
         framework, framework_version, domain, task, min_hardware_generation, cpu) in iterate_docker_images():
        docker_image = docker_image_model(
            name=name,
            version=version,
            url=url,
            registry_url=registry_url,
            registry_username=registry_username if (registry_username != '') else None,
            registry_password=registry_password if (registry_password != '') else None,
            cuda_version=cuda_model.objects.filter(version=Decimal(cuda_version)).first(),
            framework=framework,
            framework_version=framework_version,
            domain=domain,
            task=task,
            min_hardware_generation=hardware_model.objects.filter(generation=min_hardware_generation).first()
        )
        docker_image.save()


class Migration(migrations.Migration):
    """
    Migration inserting the Docker image presets into the database.
    """
    dependencies = [
        ('ufdl-core', '0004_hardware'),
        ('ufdl-core', '0005_cuda')
    ]

    operations = [
        migrations.RunPython(add_initial_docker_images)
    ]
