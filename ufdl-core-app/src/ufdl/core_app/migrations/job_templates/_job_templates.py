import os
import glob
from typing import Iterator, List

from ufdl.json.core.jobs import JobTemplateMigrationSpec

from ...apps import UFDLCoreAppConfig


def iterate_job_templates(path: str) -> Iterator[JobTemplateMigrationSpec]:
    """
    Iterates over the known job templates.

    :return:    An iterator over the JSON job template specifications.
    """
    for filename in glob.iglob(os.path.join(path, "*.json")):
        yield JobTemplateMigrationSpec.load_json_from_file(filename)


def get_python_job_template_migration(job_template_iterator: Iterator[JobTemplateMigrationSpec]):
    """
    Creates a migration function for adding the job templates
    from the given iterator to the database.

    :param job_template_iterator:   The iterator of job templates.
    :return:                        The migration function.
    """
    # Define the migration function
    def migration_function(apps, schema_editor):
        add_initial_job_templates(apps, schema_editor, job_template_iterator)

    return migration_function


def add_initial_job_templates(apps, schema_editor, job_template_iterator: Iterator[JobTemplateMigrationSpec]):
    """
    Adds the standard job templates to the database.

    :param apps:                    The app registry.
    :param schema_editor:           Unused.
    :param job_template_iterator:   An iterator over a job template JSON files.
    """
    # Get the required models
    input_model = apps.get_model(UFDLCoreAppConfig.label, "Input")
    parameter_model = apps.get_model(UFDLCoreAppConfig.label, "Parameter")
    framework_model = apps.get_model(UFDLCoreAppConfig.label, "Framework")
    data_domain_model = apps.get_model(UFDLCoreAppConfig.label, "DataDomain")
    job_type_model = apps.get_model(UFDLCoreAppConfig.label, "JobType")
    licence_model = apps.get_model(UFDLCoreAppConfig.label, "Licence")
    job_template_model = apps.get_model(UFDLCoreAppConfig.label, "JobTemplate")

    # Add each Docker image to the database
    for job_template in job_template_iterator:

        # Validate the licence
        licence_instance = licence_model.objects.filter(name=job_template.licence).first()
        if licence_instance is None:
            raise Exception(f"Unknown licence '{job_template.licence}'")

        # Validate the tasks
        job_type_instance = job_type_model.objects.filter(name=job_template.job_type).first()
        if job_type_instance is None:
            raise Exception(f"Unknown job-type '{job_template.job_type}'")

        # Validate the data-domain
        data_domain_instance = data_domain_model.objects.filter(name=job_template.domain).first()
        if data_domain_instance is None:
            raise Exception(f"Unknown data-domain '{job_template.domain}'")

        # Make sure the framework exists
        framework_parts = split_multipart_field(job_template.framework)
        if len(framework_parts) != 2:
            raise Exception(f"Couldn't split framework '{job_template.framework}' into name and "
                            f"version parts (separate with |)")
        framework_instance = framework_model.objects.filter(name=framework_parts[0],
                                                            version=framework_parts[1]).first()
        if framework_instance is None:
            raise Exception(f"Unknown framework {job_template.framework}")

        # Create the Docker image
        job_template_instance = job_template_model(
            name=job_template.name,
            version=1,
            description=job_template.description,
            scope=job_template.scope,
            framework=framework_instance,
            domain=data_domain_instance,
            type=job_type_instance,
            executor_class=job_template.executor_class,
            required_packages=job_template.required_packages,
            body=job_template.body,
            licence=licence_instance,
        )
        job_template_instance.save()

        # Add the inputs
        for input_spec in job_template.inputs:
            input_model(template=job_template_instance,
                        name=input_spec.name,
                        type=input_spec.type,
                        options=input_spec.options,
                        help=input_spec.help).save()

        # Add the parameters
        for parameter_spec in job_template.parameters:
            parameter_model(template=job_template_instance,
                            name=parameter_spec.name,
                            type=parameter_spec.type,
                            default=parameter_spec.default,
                            help=parameter_spec.help).save()


def split_multipart_field(field: str) -> List[str]:
    """
    Splits a multi-part field into its component parts.

    :param field:   The multi-part field's value.
    :return:        The parts.
    """
    return field.split("|", maxsplit=2)
