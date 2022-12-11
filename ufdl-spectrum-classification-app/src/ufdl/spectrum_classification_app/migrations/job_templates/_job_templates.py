import os
from typing import Iterator

from ufdl.core_app.migrations.job_templates import iterate_job_templates as core_iterate_job_templates

from ufdl.json.core.jobs import JobTemplateSpec

# The data directory containing the job template definitions
ROOT = os.path.split(__file__)[0]


def iterate_job_templates() -> Iterator[JobTemplateSpec]:
    yield from core_iterate_job_templates(ROOT)
