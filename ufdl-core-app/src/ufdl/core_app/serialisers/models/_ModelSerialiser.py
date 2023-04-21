from rest_framework import serializers

from ...models import DataDomain
from ...models.licences import Licence
from ...models.models import Model
from ..mixins import SoftDeleteModelSerialiser
from ..nodes import FrameworkSerialiser


class ModelSerialiser(SoftDeleteModelSerialiser):
    # Slug fields must be specified explicitly
    domain = serializers.SlugRelatedField("name", queryset=DataDomain.objects)
    licence = serializers.SlugRelatedField("name", queryset=Licence.objects)

    # Getting/setting data is done separately, just indicate if there is data
    data = serializers.BooleanField(read_only=True, source='has_data')

    def to_representation(self, instance: Model):
        representation = super().to_representation(instance)
        representation["framework"] = FrameworkSerialiser().to_representation(instance.framework)
        return representation

    class Meta:
        model = Model
        fields = ["pk",
                  "framework",
                  "domain",
                  "licence",
                  "data"] + SoftDeleteModelSerialiser.base_fields
