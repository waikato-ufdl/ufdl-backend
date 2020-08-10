from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from ..models import User


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username",
                  "password",
                  "pk",
                  "last_login",
                  "is_superuser",
                  "first_name",
                  "last_name",
                  "email",
                  "is_staff",
                  "is_active",
                  "node",
                  "date_joined"]
        read_only_fields = ["last_login",
                            "is_superuser",
                            "is_staff",
                            "date_joined"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        self.handle_password(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.handle_password(validated_data)
        return super().update(instance, validated_data)

    def handle_password(self, validated_data):
        password = validated_data.get("password", None)

        if password is not None:
            validated_data["password"] = make_password(password)
