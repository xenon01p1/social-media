from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    rp_otp_code = models.IntegerField(blank=True, null=True) # rp = reset password
    rp_verify_status = models.CharField(max_length=1, blank=True, null=True)
    otp_code = models.IntegerField(blank=True, null=True)
    verify_status = models.CharField(max_length=1, blank=True, null=True)
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    mute_status = models.BooleanField(default=False)
    block_status = models.BooleanField(default=False)
    follower_count = models.IntegerField(blank=True, null=True)
    following_count = models.IntegerField(blank=True, null=True)

    insert_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='inserted_users')
    insert_datetime = models.DateTimeField(auto_now_add=True)

    update_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='updated_users')
    update_datetime = models.DateTimeField(blank=True, null=True)

    delete_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='deleted_users')
    delete_datetime = models.DateTimeField(blank=True, null=True)
    delete_status = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name=_('groups'),
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user.'),
    )



