from rest_framework import serializers
from .models import Pass


class PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pass
        fields = "__all__"
