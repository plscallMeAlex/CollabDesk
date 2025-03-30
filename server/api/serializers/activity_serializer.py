from rest_framework import serializers
from api.models import Activity


class AcitvitySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Activity
        fields = ["id", "guild", "user", "detail", "created_at"]
