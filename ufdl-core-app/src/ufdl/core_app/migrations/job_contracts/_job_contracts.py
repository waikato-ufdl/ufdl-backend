import os
from typing import Iterator, Tuple

from .._util import iterate_csv_file

# The data directory containing the job-contract definitions
ROOT = os.path.split(__file__)[0]


def iterate_job_contracts() -> Iterator[Tuple[str, str, str]]:
    """
    Iterates over the known job-contracts.

    :return:    An iterator over the names of the job-contracts.
    """
    for name, pkg, cls in iterate_csv_file(os.path.join(ROOT, "job_contracts.csv")):
        yield name, pkg, cls
