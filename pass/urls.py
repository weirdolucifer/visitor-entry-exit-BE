from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PassViewSet, VisitLogViewSet, VisitLogStatsAPIView, TodayVisitorVisit, WeeklyVisitorVisit

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
    path(
        r"today-visitor-visit/",
        TodayVisitorVisit.as_view(),
        name="today_visitor_visit",
    ),
    path(
        r"weekly-visitor-visit/",
        WeeklyVisitorVisit.as_view(),
        name="weekly_visitor_visit",
    ),
]
