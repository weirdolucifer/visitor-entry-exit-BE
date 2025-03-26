from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VisitorViewSet

app_name = "visitors"

router = DefaultRouter()
router.register(r'visitor-info', VisitorViewSet, basename='visitor_info')

urlpatterns = [
    path('', include(router.urls)),
]
