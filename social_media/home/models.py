# from django.contrib.auth.models import AbstractUser
from django.db import models
from authentication.models import CustomUser

# Create your models here.

class Story(models.Model):
    file = models.CharField(max_length=255)
    insert_by =  models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="story_inserted_by")
    insert_datetime = models.DateTimeField(auto_now_add=True)
    delete_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="story_deleted_by")
    delete_datetime = models.DateTimeField(blank=True, null=True)
    delete_status = models.BooleanField(default=False)


class Seen_Story(models.Model): # list of users who has seen another user story
    story_id = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="seen_story_story_id")
    seen_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="seen_story_seen_by")
    insert_datetime = models.DateTimeField(auto_now_add=True)
