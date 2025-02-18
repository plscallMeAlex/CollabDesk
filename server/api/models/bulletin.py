from django.db import models
import uuid

class Bulletin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guild = models.ForeignKey('Guild', on_delete=models.CASCADE)
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)   
    