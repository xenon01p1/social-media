
from django.db import models
from authentication.models import CustomUser

# Create your models here.

class Messages(models.Model):
    message_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="message_from")
    message_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="deliver_to")
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(blank=True, null=True)
    read_datetime = models.DateTimeField(blank=True, null=True)
    delete_status = models.BooleanField(default=False)
    delete_datetime = models.DateTimeField(blank=True, null=True)


class CloseFriend(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friend")
    close_friend_with = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friend_with")







