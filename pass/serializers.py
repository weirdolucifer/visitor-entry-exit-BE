from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Pass, VisitLog


class PassSerializer(serializers.ModelSerializer):
    visitor_name = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Pass
        fields = [
            "id",
            "pass_type",
            "validity",
            "pass_image",
            "visitor",
            "visitor_name",
            "employee",
            "employee_name",
            "local_pass_id"
        ]

    def get_visitor_name(self, obj):
        visitor = obj.visitor
        if visitor:
            return f"{visitor.first_name} {visitor.last_name}"
        return None

    def get_employee_name(self, obj):
        employee = obj.employee
        if employee:
            return f"{employee.name}"
        return None



class VisitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitLog
        fields = '__all__'

    def validate(self, attrs):
        """
        Ensure that the pass associated with this visit log is valid (i.e., not expired).
        """
        pass_id = attrs.get('pass_id')

        if pass_id:
            if pass_id.validity <= timezone.now():
                raise ValidationError(f"The pass with ID {pass_id.id} has expired and cannot be used for a visit log.")

        return attrs
