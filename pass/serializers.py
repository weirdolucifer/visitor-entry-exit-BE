from rest_framework import serializers
from .models import Pass


class PassSerializer(serializers.ModelSerializer):
    visitor_name = serializers.SerializerMethodField()

    class Meta:
        model = Pass
        fields = [
            "id",
            "pass_type",
            "validity",
            "pass_image",
            "visitor",
            "visitor_name",
        ]

    def get_visitor_name(self, obj):
        visitor = obj.visitor
        if visitor:
            return f"{visitor.first_name} {visitor.last_name}"
        return None
