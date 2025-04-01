from django.db import models
import uuid
import random
import string


def generate_invite_token():
    """Generate a unique 8-character invite token."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


class Guild(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    invitetoken = models.CharField(
        max_length=8, unique=True, default=generate_invite_token, editable=False
    )

    def save(self, *args, **kwargs):
        # Ensure the invite token is unique
        if not self.invitetoken:
            while True:
                token = generate_invite_token()
                if not Guild.objects.filter(invitetoken=token).exists():
                    self.invitetoken = token
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
