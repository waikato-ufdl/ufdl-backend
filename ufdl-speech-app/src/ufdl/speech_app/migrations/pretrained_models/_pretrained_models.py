import os
from typing import Iterator, Tuple, Optional

from ufdl.core_app.migrations.pretrained_models import iterate_pretrained_models as core_iterate_pretrained_models

# The data directory containing the pre-trained model definitions
ROOT = os.path.split(__file__)[0]


def iterate_pretrained_models() -> Iterator[Tuple[Optional[str], ...]]:
    yield from core_iterate_pretrained_models(ROOT)
