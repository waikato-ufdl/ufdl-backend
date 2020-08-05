import os
from typing import Iterator, Tuple, Optional

from .._util import iterate_csv_file

# The data directory containing the framework definitions
ROOT = os.path.split(__file__)[0]


def iterate_frameworks() -> Iterator[Tuple[str, str]]:
    """
    Iterates over the known frameworks.

    :return:    An iterator over the following fields of the known frameworks:
                 - name
                 - version
    """
    yield from iterate_csv_file(os.path.join(ROOT, "frameworks.csv"))
