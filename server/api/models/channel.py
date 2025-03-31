from django.db import models
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
        default=None  # Default is NULL unless set explicitly
    )

    def save(self, *args, **kwargs):
        # Auto-generate wsroom only if the channel is "text"
        if self.channel_type == "text" and not self.wsroom:
            self.wsroom = uuid.uuid4().hex[:8]

        super().save(*args, **kwargs)