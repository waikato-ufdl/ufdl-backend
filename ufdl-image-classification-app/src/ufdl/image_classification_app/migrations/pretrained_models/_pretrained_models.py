import os
from typing import Iterator

from ufdl.json.core.models import PretrainedModelMigrationSpec

from ufdl.core_app.migrations.pretrained_models import iterate_pretrained_models as core_iterate_pretrained_models

# The data directory containing the pre-trained model definitions
ROOT = os.path.split(__file__)[0]


def iterate_pretrained_models() -> Iterator[PretrainedModelMigrationSpec]:
    yield from core_iterate_pretrained_models(ROOT)
