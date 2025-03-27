from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PassViewSet

app_name = "passes"

router = DefaultRouter()
router.register(r"visitor-pass-info", PassViewSet, basename="visitor_info")

urlpatterns = [
    path("", include(router.urls)),
]
