from rest_framework import serializers

from ..models import LogEntry


class LogEntrySerialiser(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ["pk",
                  "creation_time",
                  "level",
                  "is_internal",
                  "message"]
        read_only_fields = ["creation_time", "is_internal"]
