from django.db import models
import uuid

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)
    guild = models.ForeignKey("Guild", on_delete=models.CASCADE)