from django.db import models

class ChannelRole(models.Model):
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)