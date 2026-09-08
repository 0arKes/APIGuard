from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase

from monitoring.choices import APIStatus
from monitoring.models import API, History
from monitoring.services.api_response_services import (
    save_history,
    verify_api_response,
)


class VerifyAPIResponseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usertest",
            password="A1B2C3D4@",
        )
        self.api = API.objects.create(
            nickname="api-test",
            url="https://example.com",
            owner=self.user,
        )

    @patch("monitoring.services.api_response_services.requests.get")
    def test_api_response_up(self, mock_get):
        response = Mock()
        response.status_code = 200
        response.reason = "OK"
        response.elapsed.total_seconds.return_value = 0.150
        mock_get.return_value = response

        result = verify_api_response(self.api)

        self.assertEqual(result.api_response, "OK")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.response_time, 150)
        self.assertEqual(result.api_status, APIStatus.UP)
        self.assertEqual(result.timeout_count, 0)

    @patch("monitoring.services.api_response_services.requests.get")
    def test_api_response_down(self, mock_get):
        response = Mock()
        response.status_code = 500
        response.reason = "Internal Server Error"
        response.elapsed.total_seconds.return_value = 0.200
        mock_get.return_value = response

        result = verify_api_response(self.api)

        self.assertEqual(result.api_response, "Internal Server Error")
        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.response_time, 200)
        self.assertEqual(result.api_status, APIStatus.DOWN)
        self.assertEqual(result.timeout_count, 0)

    @patch("monitoring.services.api_response_services.requests.get")
    def test_api_response_timeout(self, mock_get):
        import requests

        mock_get.side_effect = requests.exceptions.Timeout

        result = verify_api_response(self.api)

        self.assertEqual(result.api_response, "Timeout")
        self.assertEqual(result.timeout_count, 1)
        self.assertEqual(result.api_status, APIStatus.UNKNOWN)

    @patch("monitoring.services.api_response_services.requests.get")
    def test_api_response_three_timeouts(self, mock_get):
        import requests

        self.api.timeout_count = 2
        self.api.save()

        mock_get.side_effect = requests.exceptions.Timeout

        result = verify_api_response(self.api)

        self.assertEqual(result.api_response, "Timeout")
        self.assertEqual(result.timeout_count, 3)
        self.assertEqual(result.api_status, APIStatus.DOWN)

    @patch("monitoring.services.api_response_services.requests.get")
    def test_api_response_reset_timeout_count(self, mock_get):
        self.api.timeout_count = 2
        self.api.save()

        response = Mock()
        response.status_code = 200
        response.reason = "OK"
        response.elapsed.total_seconds.return_value = 0.100
        mock_get.return_value = response

        result = verify_api_response(self.api)

        self.assertEqual(result.timeout_count, 0)
        self.assertEqual(result.api_status, APIStatus.UP)

    @patch("monitoring.services.api_response_services.requests.get")
    def test_api_response_connection_error(self, mock_get):
        import requests

        mock_get.side_effect = requests.exceptions.ConnectionError

        result = verify_api_response(self.api)

        self.assertEqual(result.api_response, "Connection Error")
        self.assertEqual(result.api_status, APIStatus.DOWN)
        self.assertEqual(result.timeout_count, 0)


class SaveHistoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usertest",
            password="A1B2C3D4@",
        )
        self.api = API.objects.create(
            nickname="api-test",
            url="https://example.com",
            owner=self.user,
        )

    def test_save_history(self):
        result = Mock()
        result.api_response = "OK"
        result.status_code = 200
        result.response_time = 150
        result.api_status = APIStatus.UP
        result.timeout_count = 0

        save_history(result, self.api)

        history = History.objects.get(api=self.api)

        self.assertEqual(history.api_response, "OK")
        self.assertEqual(history.status_code, 200)
        self.assertEqual(history.response_time, 150)

    def test_save_history_updates_api(self):
        result = Mock()
        result.api_response = "Timeout"
        result.status_code = None
        result.response_time = None
        result.api_status = APIStatus.DOWN
        result.timeout_count = 3

        save_history(result, self.api)

        self.api.refresh_from_db()

        self.assertEqual(self.api.api_status, APIStatus.DOWN)
        self.assertEqual(self.api.timeout_count, 3)
