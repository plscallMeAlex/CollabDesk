from django.db import models

class GuildMembership(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    guild = models.ForeignKey('Guild', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)