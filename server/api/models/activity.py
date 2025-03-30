from django.db import models
import uuid


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guild = models.ForeignKey("Guild", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True)
    detail = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
