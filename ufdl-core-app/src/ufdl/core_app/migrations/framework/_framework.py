import os
from typing import Iterator, Tuple

from ...apps import UFDLCoreAppConfig
from .._util import iterate_csv_file


def iterate_frameworks(path: str) -> Iterator[Tuple[str, str]]:
    """
    Iterates over the known frameworks.

    :param path:    The path to the frameworks.csv file.
    :return:        An iterator over the following fields of the known frameworks:
                     - name
                     - version
    """
    yield from iterate_csv_file(os.path.join(path, "frameworks.csv"))


def get_python_docker_migration(framework_iterator: Iterator[Tuple[str, str]]):
    """
    Creates a migration function for adding the frameworks
    from the given iterator to the database.

    :param framework_iterator:      The iterator of frameworks.
    :return:                        The migration function.
    """
    # Define the migration function
    def migration_function(apps, schema_editor):
        add_initial_frameworks(apps, schema_editor, framework_iterator)

    return migration_function


def add_initial_frameworks(apps, schema_editor, framework_iterator: Iterator[Tuple[str, str]]):
    """
    Adds the standard frameworks to the database.

    :param apps:                The app registry.
    :param schema_editor:       Unused.
    :param framework_iterator:  The iterator of frameworks.
    """
    # Get the Framework model
    framework_model = apps.get_model(UFDLCoreAppConfig.label, "Framework")

    # Add each framework version to the database
    for name, version in framework_iterator:
        # Skip this framework if it already exists
        if framework_model.objects.filter(name=name, version=version).exists():
            continue

        framework = framework_model(name=name, version=version)
        framework.save()
