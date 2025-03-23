from django.urls import path

from account.views import LoginAPIView

app_name = "accounts"

urlpatterns = [
    path(
        r"login-user/",
        LoginAPIView.as_view(),
        name="login_user",
    ),
]