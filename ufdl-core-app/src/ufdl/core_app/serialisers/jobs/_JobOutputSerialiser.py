from ...models.jobs import JobOutput
from ..mixins import SoftDeleteModelSerialiser


class JobOutputSerialiser(SoftDeleteModelSerialiser):
    class Meta:
        model = JobOutput
        fields = ["pk",
                  "name",
                  "type"] + SoftDeleteModelSerialiser.base_fields
