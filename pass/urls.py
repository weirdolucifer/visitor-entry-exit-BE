from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PassViewSet, VisitLogViewSet, VisitLogStatsAPIView

app_name = "passes"

router = DefaultRouter()
router.register(r"pass-info", PassViewSet, basename="pass_info")
router.register(r"visit-log", VisitLogViewSet, basename="visit_log")

urlpatterns = [
    path("", include(router.urls)),
    path(
        r"visit-stats/",
        VisitLogStatsAPIView.as_view(),
        name="visit_stats",
    ),
]
