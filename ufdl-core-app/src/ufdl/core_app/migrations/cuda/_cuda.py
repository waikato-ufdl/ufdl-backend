import os
from decimal import Decimal
from typing import Iterator, Tuple

from .._util import iterate_csv_file

# The data directory containing the CUDA definitions
ROOT = os.path.split(__file__)[0]


def iterate_cuda() -> Iterator[Tuple[Decimal, str, str]]:
    """
    Iterates over the known CUDA versions.

    :return:    An iterator over the versions, full-versions and min-driver-versions
                of the CUDA versions.
    """
    for version, full_version, min_driver_version in iterate_csv_file(os.path.join(ROOT, "cuda.csv")):
        yield Decimal(version), full_version, min_driver_version
