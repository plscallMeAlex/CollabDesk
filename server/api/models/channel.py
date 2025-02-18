from django.db import models
import uuid

class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    guild = models.ForeignKey("Guild", on_delete=models.CASCADE)