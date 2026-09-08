from django.contrib.auth.models import User
from django.test import TestCase

from monitoring.models import API, History


class APITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="usertest", password="A1B2C3D4@")

        self.api = API.objects.create(
            nickname="api-test", url="https://example.com", owner=self.user
        )

    def test_api_values(self):
        self.assertEqual(str(self.api), "api-test")
        self.assertEqual(self.api.api_status, "UNKNOWN")
        self.assertEqual(self.api.timeout_count, 0)

    def test_api_owner(self):
        self.assertEqual(self.api.owner, self.user)


class HistoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="usertest", password="A1B2C3D4@")

        self.api = API.objects.create(
            nickname="api-test", url="https://example.com", owner=self.user
        )

        self.history = History.objects.create(
            api_response="OK", status_code=200, response_time=150, api=self.api
        )

    def test_history(self):
        self.assertEqual(self.history.api, self.api)
        self.assertEqual(self.history.api_response, "OK")
        self.assertEqual(self.history.status_code, 200)
        self.assertEqual(self.history.response_time, 150)
        self.assertIsNotNone(self.history.date)

    def test_history_related_to_api(self):
        self.assertEqual(self.api.histories.count(), 1)
        self.assertEqual(self.api.histories.first(), self.history)

    def test_delete_api_deletes_history(self):
        self.api.delete()
        self.assertFalse(History.objects.filter(id=self.history.id).exists())
