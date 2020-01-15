from rest_framework import serializers
from ..models.files import NamedFile


class NamedFileSerialiser(serializers.BaseSerializer):
    def to_representation(self, instance):
        # Make sure the instance is a named file
        if not isinstance(instance, NamedFile):
            raise TypeError(f"Expected a NamedFile but got a {type(instance).__name__}")

        return {
            "filename": instance.filename
        }
