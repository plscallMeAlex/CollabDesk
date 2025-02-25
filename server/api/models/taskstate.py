from django.db import models
import uuid


class TaskState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20)
    guild = models.ForeignKey(
        "Guild", on_delete=models.CASCADE, related_name="taskstate_guild"
    )
