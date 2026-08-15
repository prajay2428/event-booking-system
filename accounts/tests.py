from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class AccountApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "member", email="member@example.com", password="safe-password"
        )

    def test_login_accepts_email_and_current_user_uses_session(self):
        response = self.client.post(
            "/api/accounts/login",
            {"username": "member@example.com", "password": "safe-password"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/api/accounts/me").data["id"], self.user.id)

    def test_login_requires_credentials(self):
        response = self.client.post(
            "/api/accounts/login", {}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_csrf_endpoint_sets_cookie(self):
        response = self.client.get("/api/accounts/csrf")
        self.assertEqual(response.status_code, 200)
        self.assertIn("csrftoken", response.cookies)

    def test_authenticated_api_post_accepts_csrf_cookie(self):
        client = Client(enforce_csrf_checks=True)
        client.get("/api/accounts/csrf")
        token = client.cookies["csrftoken"].value
        client.post(
            "/api/accounts/login",
            {"username": "member", "password": "safe-password"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

        rotated_token = client.cookies["csrftoken"].value
        response = client.post(
            "/api/accounts/logout",
            content_type="application/json",
            HTTP_X_CSRFTOKEN=rotated_token,
        )
        self.assertEqual(response.status_code, 200)
