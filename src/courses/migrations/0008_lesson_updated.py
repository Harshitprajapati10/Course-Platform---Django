# Generated by Django 5.1.2 on 2024-11-20 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_alter_lesson_options_lesson_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
