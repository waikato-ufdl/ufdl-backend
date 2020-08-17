import os
from decimal import Decimal
from typing import Iterator, Tuple, Optional

from ...apps import UFDLCoreAppConfig
from .._util import iterate_csv_file

# The data directory containing the Docker image definitions
ROOT = os.path.split(__file__)[0]


def iterate_docker_images(path: str = os.path.join(ROOT, "docker_images.csv")) -> Iterator[Tuple[Optional[str], ...]]:
    """
    Iterates over the known Docker images.

    :return:    An iterator over the following fields of the known Docker images:
                 - name
                 - version
                 - URL
                 - registry URL
                 - registry username
                 - registry password
                 - CUDA version
                 - framework
                 - framework version
                 - domain
                 - tasks
                 - minimum hardware generation
                 - cpu
                 - license
    """
    yield from iterate_csv_file(path)


def get_python_docker_migration(docker_image_iterator):
    """
    Creates a migration function for adding the Docker images
    from the given iterator to the database.

    :param docker_image_iterator:   The iterator of Docker images.
    :return:                        The migration function.
    """
    # Define the migration function
    def migration_function(apps, schema_editor):
        add_initial_docker_images(apps, schema_editor, docker_image_iterator)

    return migration_function


def add_initial_docker_images(apps, schema_editor, docker_image_iterator):
    """
    Adds the standard Docker images to the database.

    :param apps:                    The app registry.
    :param schema_editor:           Unused.
    :param docker_image_iterator:   An iterator over a docker image CSV file.
    """
    # Get the required models
    hardware_model = apps.get_model(UFDLCoreAppConfig.label, "Hardware")
    cuda_model = apps.get_model(UFDLCoreAppConfig.label, "CUDAVersion")
    docker_image_model = apps.get_model(UFDLCoreAppConfig.label, "DockerImage")
    framework_model = apps.get_model(UFDLCoreAppConfig.label, "Framework")
    data_domain_model = apps.get_model(UFDLCoreAppConfig.label, "DataDomain")
    job_type_model = apps.get_model(UFDLCoreAppConfig.label, "JobType")
    licence_model = apps.get_model(UFDLCoreAppConfig.label, "Licence")

    # Add each Docker image to the database
    for (name, version, url, registry_url, registry_username, registry_password, cuda_version,
         framework, framework_version, domain, tasks, min_hardware_generation, cpu, license) in docker_image_iterator:

        # Validate the licence
        licence_instance = licence_model.objects.filter(name=license).first()
        if licence_instance is None:
            raise Exception(f"Unknown licence '{license}'")

        # Validate the tasks
        tasks = tasks.split(",")
        job_types = []
        for task in tasks:
            job_type_instance = job_type_model.objects.filter(name=task).first()
            if job_type_instance is None:
                raise Exception(f"Unknown job-type '{task}'")
            job_types.append(job_type_instance)

        # Validate the data-domain
        data_domain_instance = data_domain_model.objects.filter(name=domain).first()
        if data_domain_instance is None:
            raise Exception(f"Unknown data-domain '{domain}'")

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

        # Create the Docker image
        docker_image = docker_image_model(
            name=name,
            version=version,
            url=url,
            registry_url=registry_url,
            registry_username=registry_username,
            registry_password=registry_password,
            cuda_version=cuda_instance,
            framework=framework_instance,
            domain=data_domain_instance,
            min_hardware_generation=min_hardware_generation_instance,
            cpu=cpu,
            licence=licence_instance
        )
        docker_image.save()

        # Add the job-types
        for job_type in job_types:
            docker_image.tasks.add(job_type)
