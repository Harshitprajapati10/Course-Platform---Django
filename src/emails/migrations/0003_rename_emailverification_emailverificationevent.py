# Generated by Django 5.1.2 on 2024-11-24 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_email_active'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmailVerification',
            new_name='EmailVerificationEvent',
        ),
    ]
