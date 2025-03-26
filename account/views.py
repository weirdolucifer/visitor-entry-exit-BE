from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout


class LoginAPIView(APIView):
    """Login API view to generate and return access and refresh tokens dynamically."""

    def post(self, request, *args, **kwargs):
        """Handle login and return dynamically generated access and refresh tokens for the user."""

        # Get the username and password from the request
        username = request.data.get("username")
        password = request.data.get("password")

        # Fetch the user from the database (you've created this user in the shell)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if the password is correct
        if not user.check_password(password):
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate the refresh token for the user
        refresh = RefreshToken.for_user(user)

        # Access token is part of the refresh token object
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Create the response data with the user info and generated tokens
        user_data = {
            "id": user.id,
            "username": user.username,
            "user_type": "admin",  # You can adjust this as needed
            "image": "/path/to/profile_image.jpg",  # You can adjust this as needed
            "token": {"access": access_token, "refresh": refresh_token},
            "userInfo": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }

        return Response(user_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logout(request)
            return Response(
                {"detail": "Logged out successfully."}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"detail": f"Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
