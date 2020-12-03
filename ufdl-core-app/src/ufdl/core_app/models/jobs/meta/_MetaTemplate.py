import json
from typing import Optional, Dict, Iterator

from django.db import models
from ufdl.json.core.jobs import JobTemplateSpec, ValueTypePair
from ufdl.json.core.jobs.meta import DependencyGraph, Node, Dependency
from ufdl.json.core.jobs.notification import NotificationOverride
from wai.json.object import Absent

from ....exceptions import InvalidJobInput
from ..._User import User
from .._Job import Job
from .._JobTemplate import JobTemplate, JobTemplateQuerySet
from ._MetaTemplateChildRelation import MetaTemplateChildRelation


class MetaTemplateQuerySet(JobTemplateQuerySet):
    """
    A query-set over meta-job templates.
    """
    pass


class MetaTemplate(JobTemplate):
    """
    A meta-job template.
    """
    objects = MetaTemplateQuerySet.as_manager()

    @property
    def child_names(self) -> Iterator[str]:
        """
        Gets the names of all direct children of this meta-template.
        """
        for child_relation in self.child_relations.all():
            yield child_relation.name

    @property
    def descendant_names(self) -> Iterator[str]:
        """
        Gets the names of all descendants of this meta-template.
        """
        for child_relation in self.child_relations.all():
            # Get the direct child name
            child_name = child_relation.name

            # Yield the direct child name
            yield child_name

            # Get the child template
            child_template = child_relation.child

            # If the child is also a parent, yield its descendants as well
            if isinstance(child_template, MetaTemplate):
                for descendant_name in child_template.descendant_names:
                    yield f"{child_name}:{descendant_name}"

    def create_job(
            self,
            user: User,
            parent: Optional[Job],
            input_values: Dict[str, Dict[str, str]],
            parameter_values: Dict[str, str],
            description: Optional[str] = None,
            notification_override: Optional[NotificationOverride] = None,
            child_notification_overrides: Optional[Dict[str, NotificationOverride]] = None
    ) -> Job:
        # Check all inputs values are present and of a valid type
        if parent is None:
            self.check_input_values(input_values)

        # Create the managing meta-job
        meta_job = Job(
            template=self,
            parent=parent,
            input_values=json.dumps(input_values),
            parameter_values=json.dumps(parameter_values),
            description=description if description is not None else "",
            creator=user
        )
        meta_job.save()

        # Add the notification override for this job and any children
        meta_job.set_notifications_from_override(notification_override)
        if child_notification_overrides is not None:
            meta_job.attach_notification_overrides(child_notification_overrides)

        # Get the children which have no dependencies
        dependencyless_children = (
            self.child_relations
                .annotate(num_dependencies=models.Count('dependencies'))
                .filter(num_dependencies=0)
        )

        # Create all sub-jobs with no dependencies
        for child in dependencyless_children.all():
            self.create_sub_job(
                meta_job,
                child
            )

        return meta_job

    def create_sub_job(
            self,
            parent_job: Job,
            child_relation: MetaTemplateChildRelation,
            job_dependencies: Optional[Dict[str, Job]] = None
    ) -> Job:
        """
        Creates a sub-job for this meta-template using the provided child,
        and output values from the provided job-dependencies.

        :param parent_job:
                    The parent meta-job controlling the execution of this
                    meta-template.
        :param child_relation:
                    The child-relation to the child template to execute.
        :param job_dependencies:
                    A map containing the jobs from which the new child
                    should draw its required inputs.
        :return:
                    The created child job.
        """
        # Get the input values that apply to this sub-job
        input_values = json.loads(parent_job.input_values)
        child_input_values = {}
        for input in child_relation.child.inputs.all():
            # Get the name of the correlated input on the parent
            parent_input_name = f"{child_relation.name}:{input.name}"

            # If a value is provided directly, for the input, use it
            if parent_input_name in input_values:
                child_input_values[input.name] = input_values[parent_input_name]
                continue

            # If no dependency-jobs are provided, there is no way to get a value for this input
            if job_dependencies is None:
                raise InvalidJobInput(
                    "Tried to create dependent sub-job without dependencies"
                )

            # Get the dependency of this template that should provide the input
            dependency = child_relation.dependencies.filter(input=input).first()

            # Get the name of the dependency
            dependency_name = dependency.dependency.name

            # Get the job that should provide the output for this input
            job_dependency = job_dependencies[dependency_name]

            # Make sure the job-dependency is present
            if job_dependency is None:
                raise InvalidJobInput(
                    f"Tried to create dependent sub-job without dependency '{dependency_name}'"
                )
            elif not job_dependency.is_finished:
                raise InvalidJobInput(
                    f"Tried to create dependent sub-job when dependency '{dependency_name}' "
                    f"is not finished"
                )

            # Get the name and type of the output this input depends on
            output_dependency_name, output_dependency_type = dependency.output.split("\n")

            # Get the output dependency from the job
            output_dependency = job_dependency.outputs.filter(
                name=output_dependency_name,
                type=output_dependency_type
            ).first()

            # Make sure the output exists
            if output_dependency is None:
                raise InvalidJobInput(
                    f"Job-dependency '{dependency_name}' produced no output "
                    f"'{output_dependency_name}' of type {output_dependency_type}"
                )

            # Add the job's output as the input value
            child_input_values[input.name] = {
                "value": str(output_dependency.pk),
                "type": f"job_output<{output_dependency_type}>"
            }

        # Get the parameter values that apply to this sub-job
        parameter_values = json.loads(parent_job.parameter_values)
        child_parameter_values = {}
        for parameter in child_relation.child.parameters.all():
            parent_parameter_name = f"{child_relation.name}:{parameter.name}"
            child_parameter_values[parameter.name] = (
                parameter_values[parent_parameter_name]
                if parent_parameter_name in parameter_values else
                self.get_parameter_by_name(parent_parameter_name).default
            )

        # Get the fully-qualified name of the new job in its parent hierarchy
        full_child_name = (
            f"{parent_job.full_child_name}:{child_relation.name}"
            if parent_job.has_parent else
            child_relation.name
        )

        # Get the notification overrides for this child from the top-level parent
        override = (
            parent_job
                .top_level_parent
                .notification_overrides
                .with_name(full_child_name)
                .first()
        )

        # Convert the overrides to JSON
        if override is not None:
            override = NotificationOverride.from_json_string(override.override)

        # Create the child job
        child_job = child_relation.child.create_job(
            parent_job.creator,
            parent_job,
            child_input_values,
            child_parameter_values,
            f"child job '{child_relation.name}' of meta-job {self.name_and_version}",
            override
        )

        return child_job

    def to_json(self) -> JobTemplateSpec:
        return JobTemplateSpec(
            name=self.name,
            version=self.version,
            description=self.description,
            scope=self.scope,
            licence=self.licence.name,
            domain=(
                self.domain.name
                if self.domain is not None else
                Absent
            ),
            remaining=DependencyGraph(
                nodes={
                    child.name: Node(
                        name=child.template.name,
                        version=child.template.version,
                        parameter_defaults={
                            parameter.default
                            for parameter in self.parameters
                            if parameter.name.startswith(f"{child.name}:")
                        }
                    )
                    for child in self.child_relations
                },
                dependencies=[
                    Dependency(
                        from_node=dependency.dependency.name,
                        from_output=ValueTypePair(**{
                            key: value for key, value in zip(("value", "type"), dependency.output.split("\n"))
                        }),
                        to_node=dependency.dependent.name,
                        to_input=dependency.input.name
                    )
                    for child in self.child_relations
                    for dependency in child.dependencies
                ]
            )
        )

    def get_child(self, name: str) -> Optional[JobTemplate]:
        """
        Gets the child job-template with the given name.

        :param name:
                    The name of the child.
        :return:
                    The child job-template.
        """
        # Get the child-relation for the name
        relation = self.child_relations.with_name(name).select_related("child").first()

        # If there's no relation, there's no child
        if relation is None:
            return None

        return relation.child

    def get_descendant(self, name: str) -> Optional[JobTemplate]:
        """
        Gets a descendant template by fully-qualified name.

        :param name:
                    The fully-qualified name of the descendant.
        :return:
                    The descendant template, or None
                    if name is not a descendant.
        """
        # Split the name of the top-most child from the fully-qualified name
        if ":" in name:
            head, tail = name.split(sep=":", maxsplit=1)
        else:
            head, tail = name, None

        # Get the child with the given name
        child = self.get_child(head)

        # If there are no more name parts to process, return the child
        if tail is None:
            return child

        # If the child has no children, return None
        if not isinstance(child, MetaTemplate):
            return None

        return child.get_descendant(tail)
