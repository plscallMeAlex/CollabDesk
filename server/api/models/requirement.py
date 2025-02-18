from django.db import models
import uuid

class Requirement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guild = models.ForeignKey('Guild', on_delete=models.CASCADE)
    parentReq = models.ForeignKey('Requirement', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=50)