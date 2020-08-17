from typing import Iterator, Tuple

from ...apps import UFDLCoreAppConfig
from .._util import iterate_csv_file


def iterate_pretrained_models(path: str) -> Iterator[Tuple[str, ...]]:
    """
    Iterates over the known pre-trained models.

    :return:    An iterator over the following fields of the known pre-trained models:
                 - name
                 - description
                 - URL
                 - licence
                 - framework name
                 - framework version
                 - domain
                 - source URL
    """
    yield from iterate_csv_file(path)


def get_python_pretrained_model_migration(pretrained_model_iterator):
    """
    Creates a migration function for adding the pre-trained models
    from the given iterator to the database.

    :param pretrained_model_iterator:   The iterator of pre-trained models.
    :return:                            The migration function.
    """
    # Define the migration function
    def migration_function(apps, schema_editor):
        add_initial_pretrained_models(apps, schema_editor, pretrained_model_iterator)

    return migration_function


def add_initial_pretrained_models(apps, schema_editor, pretrained_model_iterator):
    """
    Adds the standard pre-trained models to the database.

    :param apps:                        The app registry.
    :param schema_editor:               Unused.
    :param pretrained_model_iterator:   An iterator over a pre-trained model CSV file.
    """
    # Get the required models
    named_file_model = apps.get_model(UFDLCoreAppConfig.label, "NamedFile")
    filename_model = apps.get_model(UFDLCoreAppConfig.label, "Filename")
    framework_model = apps.get_model(UFDLCoreAppConfig.label, "Framework")
    data_domain_model = apps.get_model(UFDLCoreAppConfig.label, "DataDomain")
    pretrained_model_model = apps.get_model(UFDLCoreAppConfig.label, "PreTrainedModel")
    licence_model = apps.get_model(UFDLCoreAppConfig.label, "Licence")

    # Add each Docker image to the database
    for (name, description, url, licence,
         framework_name, framework_version, domain, source) in pretrained_model_iterator:

        # Validate the licence
        licence_instance = licence_model.objects.filter(name=licence).first()
        if licence_instance is None:
            raise Exception(f"Unknown licence '{licence}'")

        # Validate the data-domain
        data_domain_instance = data_domain_model.objects.filter(name=domain).first()
        if data_domain_instance is None:
            raise Exception(f"Unknown data-domain '{domain}'")

        # Make sure the framework exists
        framework_instance = framework_model.objects.filter(name=framework_name, version=framework_version).first()
        if framework_instance is None:
            raise Exception(f"Unknown framework {framework_name} v{framework_version}")

        # Can't use methods defined on the actual NamedFile class here (i.e. 'get_association'),
        # so have to re-implement
        association = get_named_file_association(named_file_model, filename_model, source)

        # Create the pre-trained model
        pretrained_model = pretrained_model_model(
            name=name,
            description=description,
            url=url,
            framework=framework_instance,
            domain=data_domain_instance,
            licence=licence_instance,
            data=association
        )
        pretrained_model.save()


def get_named_file_association(named_file_model, filename_model, source):
    """
    Special re-implementation of NamedFile.get_association as that method is not
    accessible during migrations.

    :param named_file_model:    The NamedFile model class.
    :param filename_model:      The Filename model class.
    :param source:              The canonical source URL of the pre-trained model data.
    :return:                    A NamedFile instance.
    """
    # Get any existing association
    association = named_file_model.objects.all().filter(name__filename="model.data",
                                                        canonical_source=source).first()

    # Create a new association if it didn't exist already
    if association is None:
        # Get an existing filename record
        filename_record = filename_model.objects.all().filter(filename="model.data").first()

        # Create a new record if it didn't exist already
        if filename_record is None:
            filename_record = filename_model(filename="model.data")
            filename_record.save()

        association = named_file_model(name=filename_record, canonical_source=source)
        association.save()

    return association
