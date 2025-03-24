from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.views import LoginAPIView, LogoutView

app_name = "accounts"

urlpatterns = [
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        r"login-user/",
        LoginAPIView.as_view(),
        name="login_user",
    ),
    path(
        r"logout-user/",
        LogoutView.as_view(),
        name="logout_user",
    ),
]
