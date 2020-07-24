import os
from typing import Iterator, Tuple, Optional

from .._util import iterate_csv_file

# The data directory containing the Docker image definitions
ROOT = os.path.split(__file__)[0]


def iterate_docker_images() -> Iterator[Tuple[Optional[str], ...]]:
    """
    Iterates over the known Docker images.

    :return:    An iterator over the following fields of the known Docker images:
                 - name
                 - version
                 - URL
                 - registry URL
                 - registry username
                 - registry password
                 - CUDA version
                 - framework
                 - framework version
                 - domain
                 - task
                 - minimum hardware generation
                 - cpu
    """
    yield from iterate_csv_file(os.path.join(ROOT, "docker_images.csv"))
