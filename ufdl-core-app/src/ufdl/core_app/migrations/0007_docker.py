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
    framework_model = apps.get_model(UFDLCoreAppConfig.label, "Framework")

    # Add each Docker image to the database
    for (name, version, url, registry_url, registry_username, registry_password, cuda_version,
         framework, framework_version, domain, task, min_hardware_generation, cpu) in iterate_docker_images():

        # Validate the cpu value
        if cpu not in {"true", "false"}:
            raise Exception(f"cpu value must be 'true' or 'false': got {cpu}")
        else:
            cpu = False if cpu == 'false' else True

        # Make sure the min_hardware_generation is only missing when cpu is true
        if min_hardware_generation == "" and cpu == "false":
            raise Exception(f"min_hardware_generation can't be empty is cpu is false (for '{name}')")

        # Set the registry username/password to null of the empty string is provided
        if registry_username == '':
            registry_username = None
        if registry_password == '':
            registry_password = None

        # Make sure the CUDA version exists
        cuda_instance = cuda_model.objects.filter(version=Decimal(cuda_version)).first()
        if cuda_instance is None:
            raise Exception(f"Unknown CUDA version {cuda_version}")

        # Make sure the framework exists
        framework_instance = framework_model.objects.filter(name=framework, version=framework_version).first()
        if framework_instance is None:
            raise Exception(f"Unknown framework {framework} v{framework_version}")

        # Make sure the hardware generation exists
        if min_hardware_generation == '':
            min_hardware_generation_instance = None
        else:
            min_hardware_generation_instance = hardware_model.objects.filter(generation=min_hardware_generation).first()
            if min_hardware_generation_instance is None:
                raise Exception(f"Unknown hardware generation {min_hardware_generation}")

        docker_image = docker_image_model(
            name=name,
            version=version,
            url=url,
            registry_url=registry_url,
            registry_username=registry_username,
            registry_password=registry_password,
            cuda_version=cuda_instance,
            framework=framework_instance,
            domain=domain,
            task=task,
            min_hardware_generation=min_hardware_generation_instance,
            cpu=cpu
        )
        docker_image.save()


class Migration(migrations.Migration):
    """
    Migration inserting the Docker image presets into the database.
    """
    dependencies = [
        ('ufdl-core', '0004_hardware'),
        ('ufdl-core', '0005_cuda'),
        ('ufdl-core', '0006_framework')
    ]

    operations = [
        migrations.RunPython(add_initial_docker_images)
    ]
