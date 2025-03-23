from django.test import TestCase
from django.urls import reverse


class TestHealthCheck(TestCase):
    """Class to test the health status, readiness check and liveliness check"""

    def setUp(self):
        """Setup the requirements for the test cases"""

        self.auth_token = "Dummy.Token.ForTesting"

    def test_health_status_api_success(self):
        """Function to test the heath status api"""

        response = self.client.get(
            reverse("health_status"),
            HTTP_AUTHORIZATION=f"Authorization {self.auth_token}",
        )
        result = response.json()
        self.assertIsInstance(result["version"], str)

    def test_readiness_status_api_success(self):
        """Function to test the readiness status api"""

        response = self.client.get(
            reverse("ready_status"),
            HTTP_AUTHORIZATION=f"Authorization {self.auth_token}",
        )
        result = response.json()
        self.assertTrue(result["Ready"])

    def test_liveliness_status_api_success(self):
        """Function to test the liveliness status api"""

        response = self.client.get(
            reverse("live_status"),
            HTTP_AUTHORIZATION=f"Authorization {self.auth_token}",
        )
        result = response.json()
        self.assertTrue(result["Live"])
