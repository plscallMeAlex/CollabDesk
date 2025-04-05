from django.db import models
import uuid


class Guild(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    invitetoken = models.CharField(
        max_length=8, unique=True, blank=True, editable=False, null=True, default=None
    )

    def save(self, *args, **kwargs):
        if not self.invitetoken:  # Only generate if empty
            self.invitetoken = uuid.uuid4().hex[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
