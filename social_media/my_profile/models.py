from django.db import models
from authentication.models import CustomUser

# Create your models here.

class Followers(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    is_following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following")

    class Meta:
        unique_together = ('is_following', 'user_id')


class Report(models.Model):
    user_report = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_report")
    report_content = models.TextField()
    insert_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="isnert_by")


