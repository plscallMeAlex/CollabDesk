import uuid
from django.db import models
from django.contrib.auth.hashers import make_password


# # Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if isinstance(self.password, bytes):  # Ensure it's a string
            self.password = self.password.decode("utf-8")

        if not self.password.startswith(
            "pbkdf2_sha256$"
        ):  # Add '$' to match full hash prefix
            self.password = make_password(self.password)  # Hash password

        super().save(*args, **kwargs)
