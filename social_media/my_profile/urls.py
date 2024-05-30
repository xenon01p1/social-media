from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.profile, name="profile"),
    path("<str:id>", views.other_profile, name="other_profile"),
    path("followers_list/", views.followers_list, name="followers_list"),
    path("followings_list/", views.followings_list, name="followings_list"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("logout_view/", views.logout_view, name="logout_view"),
    path("report/<str:id>", views.report, name="report"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
