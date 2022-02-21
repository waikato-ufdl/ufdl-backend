from rest_framework import serializers

from ...models.jobs import JobContract


class JobContractSerialiser(serializers.ModelSerializer):
    class Meta:
        model = JobContract
        fields = ["pk",
                  "name",
                  "pkg",
                  "cls"]
