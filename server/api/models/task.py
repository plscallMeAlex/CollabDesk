from django.db import models
import uuid


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guild = models.ForeignKey('Guild', on_delete=models.CASCADE)
    assigner = models.ForeignKey('User', 
                                 on_delete=models.SET_NULL, 
                                 related_name="task_assigner", 
                                 null=True
                                ) # This is the user who assigned the task
    assignee = models.ForeignKey('User', 
                                 on_delete=models.SET_NULL, 
                                 related_name="task_assignee",
                                 null=True
                                ) # This is the user who is assigned the task
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    announce_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    state = models.CharField(max_length=20)
