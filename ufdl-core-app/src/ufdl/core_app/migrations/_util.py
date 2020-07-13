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
