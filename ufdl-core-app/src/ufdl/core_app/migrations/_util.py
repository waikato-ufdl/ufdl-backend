import csv
from typing import Tuple, Iterator


def iterate_csv_file(filename: str) -> Iterator[Tuple[str, ...]]:
    """
    Iterates over the rows of a CSV file.

    :param filename:    The CSV file to open.
    :return:            An iterator of string-tuples representing the rows of the file.
    """
    # Process theCSV file
    with open(filename, "r", newline='') as file:
        # Consume the header
        file.readline()

        # Attach a CSV parser to the file
        csv_reader = csv.reader(file)

        # Yield each row in the file
        yield from csv_reader


def add_data_domain(code: str):
    """
    Creates a function which adds the given data-domain to the server.

    :param code:    The two-letter code for the domain.
    """
    # Define the adding function
    def add_function(apps, schema_editor):
        # Import the core app's config
        from ..apps import UFDLCoreAppConfig

        # Get the DataDomain model
        data_domain_model = apps.get_model(UFDLCoreAppConfig.label, "DataDomain")

        # Add the domain code to the database
        data_domain_model(name=code).save()

    return add_function
