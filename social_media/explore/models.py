from django.db import models
from authentication.models import CustomUser

# Create your models here.

class Posts(models.Model):
    name = models.CharField(max_length=255)
    caption = models.TextField()
    file_1 = models.FileField(upload_to='media', null=True, blank=True)
    file_2 = models.FileField(upload_to='media', null=True, blank=True)
    file_3 = models.FileField(upload_to='media', null=True, blank=True)
    file_4 = models.FileField(upload_to='media', null=True, blank=True)
    like_count = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    insert_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="post_inserted_by")
    insert_datetime = models.DateTimeField(auto_now_add=True)
    delete_datetime = models.DateTimeField(blank=True, null=True)
    delete_status = models.BooleanField(default=False)


class SearchLog(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)







