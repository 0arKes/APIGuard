from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from monitoring.models import API


class DashboardTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username="usertest1", password="A1B2C3D4@"
        )
        self.api_1 = API.objects.create(
            nickname="api-test-1", url="https://example.com", owner=self.user_1
        )

        self.user_2 = User.objects.create_user(
            username="usertest2", password="A1B2C3D4@"
        )
        self.api_2 = API.objects.create(
            nickname="api-test-2", url="https://example.com", owner=self.user_2
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("monitoring:dashboard"))

        self.assertEqual(response.status_code, 302)

    def test_dashboard_logged(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.get(reverse("monitoring:dashboard"))

        self.assertEqual(response.status_code, 200)

    def test_dashboard_logged_content(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.get(reverse("monitoring:dashboard"))

        self.assertContains(response, "api-test-1")
        self.assertNotContains(response, "api-test-2")

    # create view

    def test_create_requires_login(self):
        response = self.client.get(reverse("monitoring:create_api"))

        self.assertEqual(response.status_code, 302)

    def test_create_logged(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.get(reverse("monitoring:create_api"))

        self.assertEqual(response.status_code, 200)

    def test_create_valid_data(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.post(
            reverse("monitoring:create_api"),
            {
                "nickname": "api-test-created",
                "url": "https://example.org",
            },
        )

        self.assertEqual(response.status_code, 302)

        api = API.objects.get(nickname="api-test-created")

        self.assertEqual(api.url, "https://example.org")
        self.assertEqual(api.owner, self.user_1)

    def test_create_invalid_data(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.post(
            reverse("monitoring:create_api"),
            {
                "nickname": "api-test-created",
                "url": "",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(API.objects.filter(nickname="api-test-created").exists())

    ### detail view

    def test_detail_requires_login(self):
        response = self.client.get(
            reverse("monitoring:detail_api", kwargs={"id": self.api_1.id})
        )

        self.assertEqual(response.status_code, 302)

    def test_detail_logged(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.get(
            reverse("monitoring:detail_api", kwargs={"id": self.api_1.id})
        )

        self.assertEqual(response.status_code, 200)

    def test_detail_logged_content(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.get(
            reverse("monitoring:detail_api", kwargs={"id": self.api_1.id})
        )

        self.assertContains(response, "api-test-1")
        self.assertNotContains(response, "api-test-2")

    ### edit view

    def test_edit_requires_login(self):
        response = self.client.get(
            reverse("monitoring:edit_api", kwargs={"id": self.api_1.id})
        )

        self.assertEqual(response.status_code, 302)

    def test_edit_logged(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.get(
            reverse("monitoring:edit_api", kwargs={"id": self.api_1.id})
        )

        self.assertEqual(response.status_code, 200)

    def test_edit_logged_other_user(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.get(
            reverse("monitoring:edit_api", kwargs={"id": self.api_2.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_edit_valid_data(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.post(
            reverse("monitoring:edit_api", kwargs={"id": self.api_1.id}),
            {
                "nickname": "api-test-edited",
                "url": "https://example.org",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.api_1.refresh_from_db()

        self.assertEqual(self.api_1.nickname, "api-test-edited")
        self.assertEqual(self.api_1.url, "https://example.org")

    def test_edit_invalid_data(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.post(
            reverse("monitoring:edit_api", kwargs={"id": self.api_1.id}),
            {
                "nickname": "api-test-edited",
                "url": "",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.api_1.refresh_from_db()

        self.assertEqual(self.api_1.nickname, "api-test-1")
        self.assertEqual(self.api_1.url, "https://example.com")

    ### delete view

    def test_delete_requires_login(self):
        response = self.client.get(
            reverse("monitoring:delete_api", kwargs={"id": self.api_1.id})
        )

        self.assertEqual(response.status_code, 302)

    def test_delete_logged(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.get(
            reverse("monitoring:delete_api", kwargs={"id": self.api_1.id})
        )

        self.assertFalse(API.objects.filter(id=self.api_1.id).exists())

    def test_delete_logged_other_user(self):
        self.client.login(username="usertest1", password="A1B2C3D4@")
        response = self.client.get(
            reverse("monitoring:delete_api", kwargs={"id": self.api_2.id})
        )

        self.assertEqual(response.status_code, 404)
