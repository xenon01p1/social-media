# Generated by Django 5.0.1 on 2024-02-06 04:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_profile', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='followers',
            unique_together={('is_following', 'user_id')},
        ),
    ]