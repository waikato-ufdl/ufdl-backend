import os
from typing import Iterator, Tuple, Optional

from ufdl.core_app.migrations.docker_images import iterate_docker_images as core_iterate_docker_images

# The data directory containing the Docker image definitions
ROOT = os.path.split(__file__)[0]


def iterate_docker_images() -> Iterator[Tuple[Optional[str], ...]]:
    yield from core_iterate_docker_images(os.path.join(ROOT, "docker_images.json"))
