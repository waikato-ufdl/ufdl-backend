from typing import Set

from django.db import migrations

from ..apps import UFDLCoreAppConfig
from .licences import iterate_licences, get_licence_subdescriptors
from ._util import DataMigration


def create_licence_subdescriptors(apps, model_name: str, entries: Set[str]):
    """
    Returns the set of instances that correspond to the given set of names in
    the a sub-descriptor table (limitations, conditions, permissions, domains). If
    an instance does not exist for the given name, it is automatically created.

    :param apps:        The app registry.
    :param model_name:  The table to use (limitations, conditions, permissions, domains).
    :param entries:     The set of entry names.
    :return:            The set of entries.
    """
    # Get the model corresponding to the selected table
    model = apps.get_model(UFDLCoreAppConfig.label, model_name)

    # Create the result set
    result = set()

    # Process each entry in turn
    for name in entries:
        # Get the existing instance if any
        present = model.objects.filter(name=name).first()

        # If the entry does not exist yet, create it
        if present is None:
            present = model(name=name)
            present.save()

        # Add the entry to the result set
        result.add(present)

    return result


def add_licence(apps, licence_name, licence_url):
    """
    Creates a new licence entry.

    :param apps:            The app registry.
    :param licence_name:    The name of the licence.
    :param licence_url:     The URL to the licence's homepage.
    """
    # Get the permissions, limitations, conditions and domains of the licence
    permissions, limitations, conditions, domains = get_licence_subdescriptors(licence_name)

    # Create table entries for each sub-descriptor
    permissions = create_licence_subdescriptors(apps, "Permission", permissions)
    conditions = create_licence_subdescriptors(apps, "Condition", conditions)
    limitations = create_licence_subdescriptors(apps, "Limitation", limitations)
    domains = create_licence_subdescriptors(apps, "Domain", domains)

    # Create an entry for the licence
    licence_model = apps.get_model(UFDLCoreAppConfig.label, "Licence")
    licence = licence_model(name=licence_name, url=licence_url)
    licence.save()

    # Add the sub-descriptors to the licence
    licence.permissions.add(*permissions)
    licence.limitations.add(*limitations)
    licence.conditions.add(*conditions)
    licence.domains.add(*domains)
    licence.save()

    return list()


def add_initial_licences(apps, schema_editor):
    """
    Adds the standard licences to the database.

    :param apps:            The app registry.
    :param schema_editor:   Unused.
    """
    # Process each licence in the file
    models = []
    for licence_name, licence_url in iterate_licences():
        models += add_licence(apps, licence_name, licence_url)
    return models


class Migration(migrations.Migration):
    """
    Migration inserting the licence presets into the database.
    """
    dependencies = [
        ('ufdl-core', '0002_the_rest')  # Is where the licence models are defined
    ]

    operations = [
        DataMigration(add_initial_licences)
    ]
