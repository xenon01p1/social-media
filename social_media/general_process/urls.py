from django.urls import path, include
from . import views

urlpatterns = [
    path("like/<str:id>", views.like, name="like"), # toggle like
    path("comment/<str:id>/<str:comment_content>", views.comment, name="comment"),
    path("comment_like/<str:id>", views.comment_like, name="comment_like"),
    path("favorite/<str:category_favorite_id>/<str:post_id>", views.favorite, name="favorite"),
    path("follow/<str:id>", views.follow, name="follow"),
    path("seen_story/", views.seen_story, name="seen_story"),
]