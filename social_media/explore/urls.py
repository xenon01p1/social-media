from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.explore, name="explore"),
    path("create", views.create_post, name="create_post"),
    path("create_story", views.create_story, name="create_story"),
    path("create_category_favorite", views.create_category_favorite, name="create_category_favorite"),
    path("category_favorite/<int:id>", views.category_favorite, name="category_favorite"),
    path("category_unfavorite/<int:id>", views.category_unfavorite, name="category_unfavorite"),
    path("<str:id>", views.scroll_post, name="scroll_post"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)