from django.db import models
from api.models import Guild, User


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
