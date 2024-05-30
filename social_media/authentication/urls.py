from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("register", views.register, name="register"),
    path("verify_otp", views.verify_otp_code, name="verify_otp"),
    path("register_profile", views.register_profile, name="register_profile"),
    path("forget_password", views.forget_password, name="forget_password"),
    path("rp_verify_otp_code", views.rp_verify_otp_code, name="rp_verify_otp_code"),
    path("reset_password", views.reset_password, name="reset_password"),
]

