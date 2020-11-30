import glob
import os
from typing import Iterator, Optional

from django.db import transaction
from ufdl.json.core.jobs import JobTemplateSpec, WorkableTemplateSpec
from ufdl.json.core.jobs.meta import DependencyGraph

from wai.json.object import Absent

from ...apps import UFDLCoreAppConfig
from ...util import max_value, split_multipart_field


def iterate_job_templates(path: str) -> Iterator[JobTemplateSpec]:
    """
    Iterates over the known job templates.

    :return:    An iterator over the JSON job template specifications.
    """
    # Get the files to import
    filenames = list(glob.iglob(os.path.join(path, "*.json")))

    # Sort into alphabetical order
    filenames.sort()

    return map(JobTemplateSpec.load_json_from_file, filenames)


def get_python_job_template_migration(job_template_iterator: Iterator[JobTemplateSpec]):
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


def add_initial_job_templates(apps, schema_editor, job_template_iterator: Iterator[JobTemplateSpec]):
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
    workable_template_model = apps.get_model(UFDLCoreAppConfig.label, "WorkableTemplate")
    meta_template_model = apps.get_model(UFDLCoreAppConfig.label, "MetaTemplate")
    meta_template_child_relation_model = apps.get_model(UFDLCoreAppConfig.label, "MetaTemplateChildRelation")
    meta_template_dependency_model = apps.get_model(UFDLCoreAppConfig.label, "MetaTemplateDependency")

    # Add each job template to the database
    for spec in job_template_iterator:
        add_job_template(
            spec,
            input_model,
            parameter_model,
            framework_model,
            data_domain_model,
            job_type_model,
            licence_model,
            job_template_model,
            workable_template_model,
            meta_template_model,
            meta_template_child_relation_model,
            meta_template_dependency_model
        )


@transaction.atomic
def add_job_template(
        spec: JobTemplateSpec,
        input_model,
        parameter_model,
        framework_model,
        data_domain_model,
        job_type_model,
        licence_model,
        job_template_model,
        workable_template_model,
        meta_template_model,
        meta_template_child_relation_model,
        meta_template_dependency_model
):
    """
    Adds a job-template to the database based on the provided specification.

    :param spec:
                The specification of the job-template.
    :param input_model:
                The Input model-class.
    :param parameter_model:
                The Parameter model-class.
    :param framework_model:
                The Framework model-class.
    :param data_domain_model:
                The DataDomain model-class.
    :param job_type_model:
                The JobType model-class
    :param licence_model:
                The Licence model-class.
    :param job_template_model:
                The JobTemplate model-class.
    :param workable_template_model:
                The WorkableTemplate model-class.
    :param meta_template_model:
                The MetaTemplate model-class.
    :param meta_template_child_relation_model:
                The MetaTemplateChildRelation model-class.
    :param meta_template_dependency_model:
                The MetaTemplateDependency model-class.
    :return:
                The created template.
    """
    if isinstance(spec.specific, WorkableTemplateSpec):
        return _add_workable_template(
            spec,
            input_model,
            parameter_model,
            framework_model,
            data_domain_model,
            job_type_model,
            licence_model,
            job_template_model,
            workable_template_model
        )
    else:
        return _add_meta_template(
            spec,
            input_model,
            parameter_model,
            data_domain_model,
            licence_model,
            job_template_model,
            meta_template_model,
            meta_template_child_relation_model,
            meta_template_dependency_model
        )


def _get_version(
        job_template_model,
        name: str,
        version: Optional[int],
        increment: bool = False
) -> Optional[int]:
    """
    Gets the version of a job-template by name.

    :param job_template_model:
                The JobTemplate model-class.
    :param name:
                The name of the template.
    :param version:
                An optional version of the template.
    :param increment:
                Whether to increment the version.
    :return:
                The provided version if any,
                otherwise None if there is no template by the given name,
                otherwise the maximum version of the template if increment is False,
                otherwise the maximum version plus one.
    """
    # If a version is supplied, just return it
    if version is not None:
        return version

    # Get the maximum version of the template if the name exists
    max_version = max_value(
        job_template_model.objects.filter(name=name, deletion_time__isnull=True),
        "version",
        None
    )

    return (
        None
        if max_version is None else
        max_version
        if not increment else
        max_version + 1
    )


def parse_common_specs(
        job_template_spec: JobTemplateSpec,
        licence_model,
        data_domain_model,
        job_template_model
):
    """
    Interprets the common properties of both kinds of job-template.

    :param job_template_spec:
                The spec to interpret.
    :param licence_model:
                The Licence model-class.
    :param data_domain_model:
                The DataDomain model-class.
    :param job_template_model:
                The JobTemplate model-class.
    :return:
                The licence, data-domain and version of the template.
    """
    # Validate the licence
    licence_instance = licence_model.objects.filter(name=job_template_spec.licence).first()
    if licence_instance is None:
        raise Exception(f"Unknown licence '{job_template_spec.licence}'")

    # Validate the data-domain
    data_domain_instance = None
    if job_template_spec.domain is not Absent:
        data_domain_instance = data_domain_model.objects.filter(name=job_template_spec.domain).first()
        if data_domain_instance is None:
            raise Exception(f"Unknown data-domain '{job_template_spec.domain}'")

    # Calculate the new version of the template
    new_version = _get_version(
        job_template_model,
        job_template_spec.name,
        None if job_template_spec.version is Absent else job_template_spec.version,
        True
    )
    if new_version is None:
        new_version = 1

    return licence_instance, data_domain_instance, new_version


def _add_workable_template(
        job_template_spec: JobTemplateSpec,
        input_model,
        parameter_model,
        framework_model,
        data_domain_model,
        job_type_model,
        licence_model,
        job_template_model,
        workable_template_model
):
    """
    Adds a job-template to the database from the given specification.

    :param job_template_spec:
                The JSON specification of the job-template.
    :param input_model:
                The Input model-class.
    :param parameter_model:
                The Parameter model-class.
    :param framework_model:
                The Framework model-class.
    :param data_domain_model:
                The DataDomain model-class.
    :param job_type_model:
                The JobType model-class.
    :param licence_model:
                The Licence model-class.
    :param job_template_model:
                The JobTemplate model-class.
    :param workable_template_model:
                The WorkableTemplate model-class.
    :return:
                The created WorkableTemplate instance.
    """
    # Get the common specs
    licence_instance, data_domain_instance, new_version = parse_common_specs(
        job_template_spec, licence_model, data_domain_model, job_template_model
    )

    # Validate the job-type
    job_type_instance = job_type_model.objects.filter(name=job_template_spec.specific.job_type).first()
    if job_type_instance is None:
        raise Exception(f"Unknown job-type '{job_template_spec.specific.job_type}'")

    # Make sure the framework exists
    framework_parts = split_multipart_field(job_template_spec.specific.framework)
    if len(framework_parts) != 2:
        raise Exception(f"Couldn't split framework '{job_template_spec.specific.framework}' into name and "
                        f"version parts (separate with |)")
    framework_instance = framework_model.objects.filter(name=framework_parts[0],
                                                        version=framework_parts[1]).first()
    if framework_instance is None:
        raise Exception(f"Unknown framework {job_template_spec.specific.framework}")

    # Create the template
    job_template_instance = workable_template_model(
        name=job_template_spec.name,
        version=new_version,
        description=job_template_spec.description,
        scope=job_template_spec.scope,
        domain=data_domain_instance,
        licence=licence_instance,
        framework=framework_instance,
        type=job_type_instance,
        executor_class=job_template_spec.specific.executor_class,
        required_packages=job_template_spec.specific.required_packages,
        body=job_template_spec.specific.body
    )
    job_template_instance.save()

    # Add the inputs
    for input_spec in job_template_spec.specific.inputs:
        input_model(
            template=job_template_instance,
            name=input_spec.name,
            types="\n".join(input_spec.types),
            options=input_spec.options,
            help=input_spec.help
        ).save()

    # Add the parameters
    for parameter_spec in job_template_spec.specific.parameters:
        parameter_model(
            template=job_template_instance,
            name=parameter_spec.name,
            type=parameter_spec.type,
            default=parameter_spec.default,
            help=parameter_spec.help
        ).save()

    return job_template_instance


def _add_meta_template(
        spec: JobTemplateSpec,
        input_model,
        parameter_model,
        data_domain_model,
        licence_model,
        job_template_model,
        meta_template_model,
        meta_template_child_relation_model,
        meta_template_dependency_model
):
    """
    Adds a job-template to the database from the given specification.

    TODO: Check for cyclic dependencies.

    :param spec:
                The JSON specification of the job-template.
    :param input_model:
                The Input model-class.
    :param parameter_model:
                The Parameter model-class.
    :param data_domain_model:
                The DataDomain model-class.
    :param licence_model:
                The Licence model-class.
    :param job_template_model:
                The JobTemplate model-class.
    :param meta_template_model:
                The MetaTemplate model-class.
    :param meta_template_child_relation_model:
                The MetaTemplateChildRelation model-class.
    :param meta_template_dependency_model:
                The MetaTemplateDependency model-class.
    :return:
                The created meta-template.
    """
    # Get the common specs
    licence_instance, data_domain_instance, new_version = parse_common_specs(
        spec, licence_model, data_domain_model, job_template_model
    )

    # Create the base template instance
    job_template_instance = meta_template_model(
        name=spec.name,
        version=new_version,
        description=spec.description,
        scope=spec.scope,
        domain=data_domain_instance,
        licence=licence_instance
    )
    job_template_instance.save()

    # Get the dependency graph from the specification
    dependency_graph: DependencyGraph = spec.specific

    # Create the child associations
    children = _add_meta_template_children(
        job_template_instance,
        dependency_graph,
        job_template_model,
        meta_template_child_relation_model
    )

    # Create the inter-dependencies
    used_inputs = _add_meta_template_dependencies(
        dependency_graph,
        children,
        meta_template_dependency_model
    )

    # Inherit inputs/parameters from our children
    _add_meta_template_inputs_and_parameters(
        job_template_instance,
        dependency_graph,
        children,
        used_inputs,
        input_model,
        parameter_model
    )

    return job_template_instance


def _add_meta_template_children(
        meta_template,
        dependency_graph: DependencyGraph,
        job_template_model,
        meta_template_child_relation_model
):
    """
    Adds the child template to a meta-template.

    :param meta_template:
                The meta-template instance.
    :param dependency_graph:
                The dependency graph specifying the children.
    :param job_template_model:
                The JobTemplate model-class.
    :param meta_template_child_relation_model:
                The MetaTemplateChildRelation model-class.
    :return:
                A mapping from child-name to child-relation.
    """
    # Keep a map of all the child-relations we create
    children = {}

    for child_name, node in dependency_graph.nodes.items():
        # Get the version of the template to call the child
        version = _get_version(
            job_template_model,
            node.name,
            node.version if node.version is not Absent else None
        )

        # Make sure the requested child template exists
        if version is None:
            raise Exception(f"Unknown child template {node.name}")

        # Get the child template instance
        child_template_instance = job_template_model.objects.filter(name=node.name, version=version).first()
        if child_template_instance is None:
            raise Exception(f"Unknown child template {node.name} v{version}")

        # Create the child association
        child = meta_template_child_relation_model(
            parent=meta_template,
            child=child_template_instance,
            name=child_name
        )
        child.save()

        # Add it to the table for later
        children[child_name] = child

    return children


def _add_meta_template_dependencies(
        dependency_graph: DependencyGraph,
        children,
        meta_template_dependency_model
):
    """
    Create the inter-dependencies between children of a meta-template.

    :param dependency_graph:
                The dependency graph specifying the inter-dependencies.
    :param children:
                Map from child-name to child-relation.
    :param meta_template_dependency_model:
                The MetaTemplateDependency model-class.
    :return:
                The set of inputs on the children that are internally connected.
    """
    # Create a set of internally-connected inputs
    used_inputs = set()

    # Process each dependency specification
    for dependency in dependency_graph.dependencies:
        # Get the name of the dependent child
        dependent_child_name = dependency.to_node

        # If the name isn't in our children, error
        if dependent_child_name not in children:
            raise Exception(f"Unknown dependent child '{dependent_child_name}'")

        # Get the dependent child
        dependent_child = children[dependent_child_name]

        # Get the name of the dependent input
        dependent_input_name = dependency.to_input

        # Get the input from the dependent child
        dependent_input = dependent_child.child.inputs.filter(name=dependent_input_name).first()

        # If the input doesn't exist, raise an error
        if dependent_input is None:
            raise Exception(
                f"Dependent child node '{dependent_child_name}' has no input "
                f"'{dependent_input_name}' to participate in pipeline"
            )

        # If the input is already marked as used, it is doubly-connected
        if dependent_input in used_inputs:
            raise Exception(
                f"Multiply-connected input '{dependent_input_name}' on child "
                f"'{dependent_child_name}'"
            )

        # If the type of the input doesn't contain the specified output type, the connection won't work
        dependent_input_types = dependent_input.types.split("\n")
        required_dependent_input_type = f"job_output<{dependency.from_output.type}>"
        if required_dependent_input_type not in dependent_input_types:
            raise Exception(
                f"Output '{dependency.from_output.value}' of node '{dependency.from_node}' is connected "
                f"to input '{dependent_input_name}' of template '{dependent_input.template.name}' "
                f"(in node '{dependent_child_name}') which doesn't accept type {required_dependent_input_type}"
            )

        # Mark the input as internally connected
        used_inputs.add(dependent_input)

        # Create the dependency
        dependency_instance = meta_template_dependency_model(
            dependency=children[dependency.from_node],
            output=f"{dependency.from_output.value}\n{dependency.from_output.type}",
            dependent=dependent_child,
            input=dependent_input
        )
        dependency_instance.save()

    return used_inputs


def _add_meta_template_inputs_and_parameters(
        meta_template_instance,
        dependency_graph: DependencyGraph,
        children,
        used_inputs,
        input_model,
        parameter_model
):
    """
    Inherits inputs and parameters for a meta-template from its children.

    :param meta_template_instance:
                The meta-template.
    :param dependency_graph:
                The dependency graph describing the child-parameter override values.
    :param children:
                The child relationships.
    :param used_inputs:
                The inputs that are internally connected.
    :param input_model:
                The Input model-class.
    :param parameter_model:
                The Parameter model-class.
    """
    # Inherit inputs/parameters from each child
    for child_name, child in children.items():
        # Create a copy of each child input
        for input in child.child.inputs.all():
            # Skip internally-connect inputs
            if input in used_inputs:
                continue

            # Create the input on the meta-template
            input_model(
                template=meta_template_instance,
                name=f"{child_name}:{input.name}",
                types=input.types,
                options=input.options,
                help=input.help
            ).save()

        # Get the parameter default overrides for this child
        default_overrides = dependency_graph.nodes[child_name].parameter_default_overrides
        if default_overrides is Absent:
            default_overrides = {}

        # Add the parameters
        for parameter in child.child.parameters.all():
            parameter_model(
                template=meta_template_instance,
                name=f"{child_name}:{parameter.name}",
                type=parameter.type,
                default=(
                    default_overrides[parameter.name]
                    if parameter.name in default_overrides else
                    parameter.default
                ),
                help=parameter.help
            ).save()