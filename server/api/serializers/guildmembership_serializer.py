from rest_framework import serializers
from api.models import GuildMembership


class GuildMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuildMembership
        fields = ["id", "user", "guild", "role", "joined_at"]

    def create(self, validated_data):
        return super().create(validated_data)
