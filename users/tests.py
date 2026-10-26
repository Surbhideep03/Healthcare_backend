from django.contrib.auth.models import User
from rest_framework.test import APITestCase

PASSWORD = "Str0ng!Pass123"


class AuthTests(APITestCase):
    def register(self, email="asha@example.com", password=PASSWORD):
        return self.client.post(
            "/api/auth/register/",
            {"name": "Asha", "email": email, "password": password},
            format="json",
        )

    def test_register_success(self):
        res = self.register()
        self.assertEqual(res.status_code, 201)
        self.assertTrue(User.objects.filter(username="asha@example.com").exists())

    def test_register_duplicate_email(self):
        self.register()
        res = self.register()
        self.assertEqual(res.status_code, 400)

    def test_register_weak_password(self):
        res = self.register(password="123")
        self.assertEqual(res.status_code, 400)

    def test_login_success(self):
        self.register()
        res = self.client.post(
            "/api/auth/login/",
            {"email": "asha@example.com", "password": PASSWORD},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_login_wrong_password(self):
        self.register()
        res = self.client.post(
            "/api/auth/login/",
            {"email": "asha@example.com", "password": "wrong"},
            format="json",
        )
        self.assertEqual(res.status_code, 401)