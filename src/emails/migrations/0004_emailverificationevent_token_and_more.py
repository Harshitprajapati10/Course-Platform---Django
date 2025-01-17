# Generated by Django 5.1.2 on 2024-11-25 09:18

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_rename_emailverification_emailverificationevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverificationevent',
            name='token',
            field=models.UUIDField(default=uuid.uuid1),
        ),
        migrations.AlterField(
            model_name='emailverificationevent',
            name='expired_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emailverificationevent',
            name='last_attempt_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
