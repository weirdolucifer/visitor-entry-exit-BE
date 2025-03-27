from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .models import Visitor
from .serializers import VisitorSerializer


class VisitorFilter(filters.FilterSet):
    name__icontains = filters.CharFilter(method="filter_name", required=False)
    phone__icontains = filters.CharFilter(
        field_name="phone", lookup_expr="icontains", required=False
    )
    gov_id_no__icontains = filters.CharFilter(
        field_name="gov_id_no", lookup_expr="icontains", required=False
    )

    class Meta:
        model = Visitor
        fields = ["phone", "gov_id_no"]

    def filter_name(self, queryset, name, value):
        if value:
            name_parts = value.split()
            return (
                queryset.filter(
                    Q(first_name__icontains=name_parts[0])
                    | Q(last_name__icontains=name_parts[0])
                )
                if len(name_parts) == 1
                else queryset.filter(
                    Q(first_name__icontains=name_parts[0])
                    & Q(last_name__icontains=name_parts[1])
                )
            )
        return queryset


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VisitorFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
