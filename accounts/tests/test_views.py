from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegisterUserTest(TestCase):
    def test_register_get(self):
        response = self.client.get(reverse("accounts:register"))

        self.assertEqual(response.status_code, 200)

    def test_register_valid_data(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "user@example.com",
                "username": "usertest",
                "password": "A1B2C3D4@",
                "password_confirmation": "A1B2C3D4@",
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:login"),
        )

        self.assertTrue(User.objects.filter(username="usertest").exists())

    def test_register_invalid_data(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "user@example.com",
                "username": "usertest",
                "password": "A1B2C3D4@",
                "password_confirmation": "different-password",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(User.objects.filter(username="usertest").exists())


class LoginUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usertest",
            password="A1B2C3D4@",
        )

    def test_login_get(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 200)

    def test_login_valid_data(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "usertest",
                "password": "A1B2C3D4@",
            },
        )

        self.assertRedirects(
            response,
            reverse("monitoring:dashboard"),
        )

    def test_login_invalid_data(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "usertest",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.wsgi_request.user.is_authenticated)


class LogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usertest",
            password="A1B2C3D4@",
        )

    def test_logout_requires_login(self):
        response = self.client.get(reverse("accounts:logout"))

        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(
            username="usertest",
            password="A1B2C3D4@",
        )

        response = self.client.get(reverse("accounts:logout"))

        self.assertRedirects(
            response,
            reverse("accounts:login"),
        )

        self.assertFalse(response.wsgi_request.user.is_authenticated)
