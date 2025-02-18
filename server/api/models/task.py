from django.db import models
import uuid

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guild = models.ForeignKey('Guild', on_delete=models.CASCADE)
    assigner = models.ForeignKey('User', on_delete=models.CASCADE, related_name="task_assigner") # This is the user who assigned the task
    assignee = models.ForeignKey('User', on_delete=models.CASCADE, related_name="task_assignee") # This is the user who is assigned the task
    created_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20)