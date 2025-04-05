from django.db import models
import uuid

class BulletinColumn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7)
    bulletin = models.ForeignKey('Bulletin', on_delete=models.CASCADE)