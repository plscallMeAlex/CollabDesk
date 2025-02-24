from rest_framework import serializers
from api.models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)
