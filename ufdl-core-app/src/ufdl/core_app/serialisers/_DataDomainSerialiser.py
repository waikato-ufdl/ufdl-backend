from rest_framework import serializers
from ..models import DataDomain


class DataDomainSerialiser(serializers.ModelSerializer):
    class Meta:
        model = DataDomain
        fields = ["pk",
                  "name"]
