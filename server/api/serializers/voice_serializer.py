from rest_framework import serializers
from api.models.channel import VoiceChannel, VoiceSession


class VoiceChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceChannel
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)


class VoiceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceSession
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)
