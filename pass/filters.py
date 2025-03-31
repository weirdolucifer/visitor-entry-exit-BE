from django_filters import rest_framework as filters
from .models import VisitLog, Pass
from django.db.models import Q


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


class VisitLogFilter(filters.FilterSet):
    visitor_name = filters.CharFilter(method="filter_visitor_name")
    whom_to_visit = filters.NumberFilter(field_name='whom_to_visit', lookup_expr='exact')
    escorted_by = filters.NumberFilter(field_name='escorted_by', lookup_expr='exact')
    in_date = filters.DateFilter(field_name='in_datetime', lookup_expr='gte')
    out_date = filters.DateFilter(field_name='out_datetime', lookup_expr='lte')
    pass_type = filters.CharFilter(field_name='pass_id__pass_type', lookup_expr='exact')
    visiting_department = filters.NumberFilter(field_name='visiting_department', lookup_expr='exact')

    class Meta:
        model = VisitLog
        fields = ['visitor_name', 'whom_to_visit', 'escorted_by', 'in_date', 'out_date', 'pass_type', 'visiting_department']

    def filter_visitor_name(self, queryset, name, value):
        if value:
            name_parts = value.split()
            if len(name_parts) == 1:
                return queryset.filter(
                    Q(pass_id__visitor__first_name__icontains=name_parts[0])
                    | Q(pass_id__visitor__last_name__icontains=name_parts[0])
                )
            elif len(name_parts) == 2:
                return queryset.filter(
                    Q(pass_id__visitor__first_name__icontains=name_parts[0])
                    & Q(pass_id__visitor__last_name__icontains=name_parts[1])
                )
        return queryset
