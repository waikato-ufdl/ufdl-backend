from rest_framework import serializers

from ...models.jobs import JobType


class JobTypeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ["pk",
                  "name"]
