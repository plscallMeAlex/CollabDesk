from rest_framework import serializers
from api.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        validated_data["password"] = validated_data["password"].encode()
        return super().create(validated_data)
