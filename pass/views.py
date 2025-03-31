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
        # Get today's date (ignoring time)
        today_start = timezone.now().date()
        today_end = today_start + timezone.timedelta(days=1)

        # Count the passes issued today (i.e., in_datetime falls within today)
        passes_issued_today = VisitLog.objects.filter(
            in_datetime__gte=today_start,
            in_datetime__lt=today_end
        ).count()

        # Current time (for comparison)
        now = timezone.now()

        # Count the number of persons still in the premises
        persons_still_in = VisitLog.objects.filter(
            in_datetime__lte=now,  # Check-in must be before or at the current time
            out_datetime__isnull=True  # They haven't checked out yet
        ).count()

        # Return both stats in a single response
        return Response({
            "passes_issued_today": passes_issued_today,
            "persons_still_in": persons_still_in
        }, status=status.HTTP_200_OK)
