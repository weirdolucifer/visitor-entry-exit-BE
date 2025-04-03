from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Pass, VisitLog


class PassSerializer(serializers.ModelSerializer):
    visitor_name = serializers.SerializerMethodField()
    visitor_image = serializers.SerializerMethodField()
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
            "visitor_image",
            "employee",
            "employee_name",
            "local_pass_id"
        ]

    def get_visitor_name(self, obj):
        visitor = obj.visitor
        if visitor:
            return f"{visitor.first_name} {visitor.last_name}"
        return None

    def get_visitor_image(self, obj):
        visitor = obj.visitor
        if visitor:
            return f"{visitor.image}"
        return None

    def get_employee_name(self, obj):
        employee = obj.employee
        if employee:
            return f"{employee.name}"
        return None



class VisitLogSerializer(serializers.ModelSerializer):
    pass_type = serializers.CharField(source='pass_id.pass_type', read_only=True)
    employee_id = serializers.IntegerField(source='pass_id.employee.id', read_only=True)
    employee_name = serializers.CharField(source='pass_id.employee.name', read_only=True)
    visitor_id = serializers.IntegerField(source='pass_id.visitor.id', read_only=True)
    visitor_name = serializers.SerializerMethodField()
    escorted_by_name = serializers.CharField(source='escorted_by.name', read_only=True)

    class Meta:
        model = VisitLog
        fields = '__all__'

    def validate(self, attrs):
        """
        Ensure that the pass associated with this visit log is valid (i.e., not expired).
        """
        pass_id = attrs.get('pass_id')
        in_datetime = attrs.get('in_datetime')

        if pass_id:
            if pass_id.validity <= timezone.now():
                raise ValidationError(f"The pass with ID {pass_id.id} has expired and cannot be used for a visit log.")

            if in_datetime and in_datetime > pass_id.validity:
                raise ValidationError(
                    f"The visit log date must be within the validity period of the pass. Pass {pass_id.id} is valid up to {pass_id.validity}.")
        return attrs

    def get_visitor_name(self, obj):
        """
        Combine the first and last name of the visitor to create a full name.
        This method is used for the `visitor_name` field in the serializer.
        """
        if obj.pass_id.visitor:
            return f"{obj.pass_id.visitor.first_name} {obj.pass_id.visitor.last_name}"
        return None
