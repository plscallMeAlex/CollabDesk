from rest_framework import serializers
from api.models import Guild


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = "__all__"