# Generated by Django 5.1.5 on 2025-02-17 15:01

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
