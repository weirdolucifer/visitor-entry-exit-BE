from django.conf import settings
from version import __version__
from rest_framework.views import APIView
from rest_framework.response import Response


class HealthStatusCheck(APIView):
    """Class to check the health status"""

    def get(self, request, **kwargs):
        """Function to get the code version"""

        response = {"version": __version__}
        return Response(response)


class ReadinessCheck(APIView):
    """Class to test the readiness of the system"""

    def get(self, request, **kwargs):
        """Function to get the readiness response"""

        response = {"Ready": True}
        return Response(response)


class LivelinessCheck(APIView):
    """Class to test the liveliness of the system"""

    def get(self, request, **kwargs):
        """Function to get the liveliness response"""

        response = {"Live": True}
        return Response(response)
