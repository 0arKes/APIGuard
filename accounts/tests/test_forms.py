from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms.auth_form import CreateUserForm, LoginUserForm


class CreateUserFormTest(TestCase):
    def test_form_valid_data(self):
        form = CreateUserForm(
            {
                "email": "user@example.com",
                "username": "usertest",
                "password": "A1B2C3D4@",
                "password_confirmation": "A1B2C3D4@",
            }
        )

        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form = CreateUserForm(
            {
                "email": "",
                "username": "",
                "password": "",
                "password_confirmation": "",
            }
        )

        self.assertFalse(form.is_valid())

    def test_form_duplicate_email(self):
        User.objects.create_user(
            username="otheruser",
            email="user@example.com",
            password="A1B2C3D4@",
        )

        form = CreateUserForm(
            {
                "email": "user@example.com",
                "username": "usertest",
                "password": "A1B2C3D4@",
                "password_confirmation": "A1B2C3D4@",
            }
        )

        self.assertFalse(form.is_valid())

    def test_form_duplicate_username(self):
        User.objects.create_user(
            username="usertest",
            email="other@example.com",
            password="A1B2C3D4@",
        )

        form = CreateUserForm(
            {
                "email": "user@example.com",
                "username": "usertest",
                "password": "A1B2C3D4@",
                "password_confirmation": "A1B2C3D4@",
            }
        )

        self.assertFalse(form.is_valid())

    def test_form_different_passwords(self):
        form = CreateUserForm(
            {
                "email": "user@example.com",
                "username": "usertest",
                "password": "A1B2C3D4@",
                "password_confirmation": "Different1@",
            }
        )

        self.assertFalse(form.is_valid())

    def test_form_invalid_password(self):
        form = CreateUserForm(
            {
                "email": "user@example.com",
                "username": "usertest",
                "password": "123456",
                "password_confirmation": "123456",
            }
        )

        self.assertFalse(form.is_valid())


class LoginUserFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usertest",
            password="A1B2C3D4@",
        )

    def test_form_valid_data(self):
        form = LoginUserForm(
            data={
                "username": "usertest",
                "password": "A1B2C3D4@",
            }
        )

        self.assertTrue(form.is_valid())

    def test_form_invalid_password(self):
        form = LoginUserForm(
            data={
                "username": "usertest",
                "password": "wrong-password",
            }
        )

        self.assertFalse(form.is_valid())

    def test_form_invalid_username(self):
        form = LoginUserForm(
            data={
                "username": "unknown-user",
                "password": "A1B2C3D4@",
            }
        )

        self.assertFalse(form.is_valid())
