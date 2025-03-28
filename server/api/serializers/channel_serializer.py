from rest_framework import serializers
from api.models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)
