import os
from typing import Iterator, Tuple

from .._util import iterate_csv_file

# The data directory containing the job-type definitions
ROOT = os.path.split(__file__)[0]


def iterate_job_types() -> Iterator[Tuple[str]]:
    """
    Iterates over the known job-types

    :return:    An iterator over the names of the job-types.
    """
    for name in iterate_csv_file(os.path.join(ROOT, "job_types.csv")):
        yield name
