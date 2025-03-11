from rest_framework import serializers
from api.models import Guild


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = ["id", "name"]

    def create(self, validated_data):
        return super().create(validated_data)
