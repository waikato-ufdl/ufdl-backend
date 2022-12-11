import os
from typing import Iterator, Tuple

from ufdl.core_app.migrations.framework import iterate_frameworks as core_iterate_frameworks

# The data directory containing the framework definitions
ROOT = os.path.split(__file__)[0]


def iterate_frameworks() -> Iterator[Tuple[str, str]]:
    yield from core_iterate_frameworks(ROOT)
