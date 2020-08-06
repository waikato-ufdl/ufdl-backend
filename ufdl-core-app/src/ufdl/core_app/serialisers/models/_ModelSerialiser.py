from rest_framework import serializers

from ...models import DataDomain
from ...models.licences import Licence
from ...models.models import Model
from ...models.nodes import Framework
from ..mixins import SoftDeleteModelSerialiser


class ModelSerialiser(SoftDeleteModelSerialiser):
    # Slug fields must be specified explicitly
    framework = serializers.SlugRelatedField("name_and_version", queryset=Framework.objects)
    domain = serializers.SlugRelatedField("name", queryset=DataDomain.objects)
    licence = serializers.SlugRelatedField("name", queryset=Licence.objects)

    # Getting/setting data is doen separately, just indicate if there is data
    data = serializers.BooleanField(read_only=True, source='has_data')

    class Meta:
        model = Model
        fields = ["pk"] + SoftDeleteModelSerialiser.base_fields
