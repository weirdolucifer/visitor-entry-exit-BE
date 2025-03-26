from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Visitor
from .serializers import VisitorSerializer

class VisitorFilter(filters.FilterSet):
    first_name__icontains = filters.CharFilter(field_name='first_name', lookup_expr='icontains', required=False)
    last_name__icontains = filters.CharFilter(field_name='last_name', lookup_expr='icontains', required=False)
    phone__icontains = filters.CharFilter(field_name='phone', lookup_expr='icontains', required=False)
    gov_id_no__icontains = filters.CharFilter(field_name='gov_id_no', lookup_expr='icontains', required=False)

    class Meta:
        model = Visitor
        fields = ['first_name', 'last_name', 'phone', 'gov_id_no']


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VisitorFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
