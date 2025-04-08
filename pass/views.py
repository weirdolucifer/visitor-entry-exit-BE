from datetime import datetime, timedelta

from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from str2bool import str2bool

from .filters import PassFilter, VisitLogFilter
from .models import Pass, VisitLog
from .serializers import PassSerializer, VisitLogSerializer


class PassViewSet(viewsets.ModelViewSet):
    queryset = Pass.objects.all().order_by("validity")
    serializer_class = PassSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PassFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        active_filter = self.request.query_params.get("active", None)
        if active_filter is not None:
            active = str2bool(active_filter)
            if active:
                queryset = queryset.filter(validity__gt=timezone.now())  # Active passes
            else:
                queryset = queryset.filter(
                    validity__lte=timezone.now()
                )  # Expired passes

        return queryset


class VisitLogViewSet(viewsets.ModelViewSet):
    queryset = VisitLog.objects.all().order_by("updated_on")
    serializer_class = VisitLogSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VisitLogFilter



class VisitLogStatsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        today_start = timezone.now().date()
        passes_issued_today = Pass.objects.filter(
            created_on__date=today_start
        ).count()

        passes_expiring_today = Pass.objects.filter(
            validity__date=today_start
        ).count()
        now = timezone.now()

        persons_still_in = VisitLog.objects.filter(
            in_datetime__lte=now,
            out_datetime__isnull=True
        ).count()

        # Return both stats in a single response
        return Response({
            "passes_issued_today": passes_issued_today,
            "passes_expiring_today": passes_expiring_today,
            "persons_still_in": persons_still_in
        }, status=status.HTTP_200_OK)


class TodayVisitorVisit(APIView):
    def get(self, request):
        today = datetime.today().date()
        visit_logs = VisitLog.objects.filter(in_datetime__date=today)

        visits = {}
        for log in visit_logs:
            adjusted_time = log.in_datetime + timedelta(hours=5, minutes=30)
            timestamp = adjusted_time.strftime("%Y-%m-%d %H:%M")

            if timestamp not in visits:
                visits[timestamp] = 0
            visits[timestamp] += 1

        return Response(visits)


class WeeklyVisitorVisit(APIView):
    def get(self, request):
        week_end = datetime.today() - timedelta(days=datetime.today().weekday())
        week_start = week_end - timedelta(days=7)

        # Query visits in the current week
        visit_logs = VisitLog.objects.filter(in_datetime__range=[week_start, week_end])

        weekly_visits = {}
        for log in visit_logs:
            date = log.in_datetime.date().strftime("%Y-%m-%d")
            if date not in weekly_visits:
                weekly_visits[date] = 0
            weekly_visits[date] += 1

        return Response(weekly_visits)
