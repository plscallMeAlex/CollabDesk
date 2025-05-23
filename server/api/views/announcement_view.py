from api.models import Announcement, Guild
from api.serializers.announcement_serializer import AnnouncementSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class AnnouncementViewSet(ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    @action(detail=False, methods=["POST"])
    def create_annoucement(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def get_announcements_by_guild(self, request):
        guild_id = request.query_params.get("guild_id")
        if guild_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        announcements = Announcement.objects.filter(guild=guild)
        if not announcements.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
