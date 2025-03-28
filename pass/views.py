from django.db.models import Q
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from str2bool import str2bool

from .models import Pass
from .serializers import PassSerializer


class PassFilter(filters.FilterSet):
    pass_type = filters.CharFilter(
        field_name="pass_type", lookup_expr="exact", required=False
    )
    visitor_name = filters.CharFilter(method="filter_name", required=False)
    visitor_id = filters.NumberFilter(
        field_name="visitor_id", lookup_expr="exact", required=False
    )

    class Meta:
        model = Pass
        fields = ["pass_type", "visitor_id", "visitor_name"]

    def filter_name(self, queryset, name, value):
        if value:
            name_parts = value.split()
            if len(name_parts) == 1:
                return queryset.filter(
                    Q(visitor__first_name__icontains=name_parts[0])
                    | Q(visitor__last_name__icontains=name_parts[0])
                )
            elif len(name_parts) == 2:
                return queryset.filter(
                    Q(visitor__first_name__icontains=name_parts[0])
                    & Q(visitor__last_name__icontains=name_parts[1])
                )
        return queryset


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
