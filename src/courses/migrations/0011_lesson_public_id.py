# Generated by Django 5.1.2 on 2024-11-21 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_course_public_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='public_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
