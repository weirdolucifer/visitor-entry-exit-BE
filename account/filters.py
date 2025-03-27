from django_filters import rest_framework as filters

from account.models import Employee, Department


class EmployeeFilter(filters.FilterSet):
    employee_id__icontains = filters.CharFilter(
        field_name="employee_id", lookup_expr="icontains", required=False
    )
    name__icontains = filters.CharFilter(
        field_name="name", lookup_expr="icontains", required=False
    )
    rank__icontains = filters.CharFilter(
        field_name="rank", lookup_expr="icontains", required=False
    )
    extension__icontains = filters.CharFilter(
        field_name="extension", lookup_expr="icontains", required=False
    )

    class Meta:
        model = Employee
        fields = ["employee_id", "name", "rank", "extension"]


class DepartmentFilter(filters.FilterSet):
    name__icontains = filters.CharFilter(
        field_name="name", lookup_expr="icontains", required=False
    )
    extension__icontains = filters.CharFilter(
        field_name="extension", lookup_expr="icontains", required=False
    )

    class Meta:
        model = Department
        fields = ["name", "extension"]
