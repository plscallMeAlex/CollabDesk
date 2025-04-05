from django.db import models
import uuid

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    sender = models.ForeignKey('User', on_delete=models.CASCADE)
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    isUnsent = models.BooleanField(default=False)
    isPinned = models.BooleanField(default=False)