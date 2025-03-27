from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .models import Pass
from .serializers import PassSerializer


class PassFilter(filters.FilterSet):
    pass_type = filters.CharFilter(
        field_name="pass_type", lookup_expr="exact", required=False
    )

    class Meta:
        model = Pass
        fields = ["pass_type"]


class PassViewSet(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PassFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
