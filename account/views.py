from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

class LoginAPIView(CreateAPIView):
    """Class to check the health status"""

    def post(self, request, **kwargs):
        """Function to get the code version"""
        response = {"status": True}
        return Response(response)
