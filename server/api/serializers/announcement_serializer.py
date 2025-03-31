from rest_framework import serializers
from api.models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Announcement
        fields = ["id", "title", "content", "guild", "user", "created_at", "author"]
