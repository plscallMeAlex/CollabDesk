from django.db import models
import uuid


class Guild(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    invitetoken = models.CharField(max_length=8, unique=True)
