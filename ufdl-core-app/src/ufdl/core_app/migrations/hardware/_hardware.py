import os
from typing import Iterator, Tuple

from .._util import iterate_csv_file

# The data directory containing the hardware definitions
ROOT = os.path.split(__file__)[0]


def iterate_hardware() -> Iterator[Tuple[str, str, str]]:
    """
    Iterates over the known hardware.

    :return:    An iterator over the generations and min/max compute-capabilities of the
                known hardware.
    """
    yield from iterate_csv_file(os.path.join(ROOT, "hardware.csv"))
