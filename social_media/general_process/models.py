from django.db import models
from explore.models import Posts
from authentication.models import CustomUser

# Create your models here.

class Likes(models.Model):
    posts_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    posts_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comments_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    like_count = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)


class Comment_like(models.Model):
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    comment_like_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)


class CategoryFavorites(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category_count = models.IntegerField(blank=True, null=True)


class Favorites(models.Model):
    category_favorite_id = models.ForeignKey(CategoryFavorites, on_delete=models.CASCADE)
    posts_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

