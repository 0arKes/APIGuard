from django.test import TestCase

from monitoring.forms.api_form import APIForm


class APIFormTest(TestCase):
    def test_form_valid_data(self):
        form = APIForm(
            {
                "nickname": "api-test",
                "url": "https://example.com",
            }
        )

        self.assertTrue(form.is_valid())

    def test_form_invalid_url(self):
        form = APIForm(
            {
                "nickname": "api-test",
                "url": "invalid-url",
            }
        )

        self.assertFalse(form.is_valid())

    def test_form_empty_nickname(self):
        form = APIForm(
            {
                "nickname": "",
                "url": "https://example.com",
            }
        )

        self.assertFalse(form.is_valid())

    def test_form_empty_url(self):
        form = APIForm(
            {
                "nickname": "api-test",
                "url": "",
            }
        )

        self.assertFalse(form.is_valid())
