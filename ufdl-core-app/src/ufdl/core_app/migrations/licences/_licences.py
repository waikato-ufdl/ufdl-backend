import csv
import os
from typing import Iterator, Tuple, Set

# The data directory containing the licence definitions
ROOT = os.path.split(__file__)[0]


def iterate_licences() -> Iterator[Tuple[str, str]]:
    """
    Iterates over the known licences.

    :return:    An iterator over the licence names and URLs.
    """
    # Process the licences in the licences file
    with open(os.path.join(ROOT, "licenses.csv"), "r", newline='') as licences_file:
        # Consume the header
        licences_file.readline()

        # Attach a CSV parser to the file
        csv_reader = csv.reader(licences_file)

        # Process each licence in the file
        for licence_name, licence_url in csv_reader:
            yield licence_name, licence_url


def get_licence_subdescriptors(licence_name: str) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Gets the permissions, limitations and conditions from a licence file.

    :param licence_name:    The name of the licence.
    :return:                The permissions, limitations and conditions of the licence.
    """
    # Create the empty return sets
    permissions, limitations, conditions = set(), set(), set()

    # Get the filename for the licence
    licence_filename = licence_name_to_file_name(licence_name)

    # Read the licence file
    with open(os.path.join(ROOT, licence_filename), "r") as licence_file:
        # Process each line in turn
        for line in licence_file:
            # Get the sub-descriptor
            subdescriptor = line[2:].strip()

            # If the line starts with 'p:', it's a permission of the licence
            if line.startswith("p:"):
                permissions.add(subdescriptor)

            # If the line starts with 'l:', it's a limitation of the licence
            elif line.startswith("l:"):
                limitations.add(subdescriptor)

            # If the line starts with 'c:', it's a condition of the licence
            elif line.startswith("c:"):
                conditions.add(subdescriptor)

    return permissions, limitations, conditions


def licence_name_to_file_name(licence_name: str) -> str:
    """
    Converts a licence name to the name of the file
    containing its definition.

    :param licence_name:    The licence name.
    :return:                The file name.
    """
    return licence_name.lower().replace(" ", "-") + ".txt"
