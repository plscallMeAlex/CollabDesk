from django.db import models
from django.contrib.auth.models import User
import uuid


class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    guild = models.ForeignKey("Guild", on_delete=models.CASCADE)
    wsroom = models.CharField(
        max_length=100,
        unique=True,
        editable=False,
        null=True,  # Allows NULL values
        blank=True,  # Allows empty values in forms
        default=None,  # Default is NULL unless set explicitly
    )

    def save(self, *args, **kwargs):
        # Auto-generate wsroom only if the channel is "text"
        if not self.wsroom:
            self.wsroom = uuid.uuid4().hex[:8]

        super().save(*args, **kwargs)


class VoiceChannel(models.Model):
    name = models.CharField(max_length=100)
    guild = models.ForeignKey(
        "Guild", on_delete=models.CASCADE, related_name="voice_channels"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VoiceSession(models.Model):
    """Track active voice sessions"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(VoiceChannel, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_muted = models.BooleanField(default=False)
    is_deafened = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "channel")
