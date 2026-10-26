from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Patient


class PatientTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="a@x.com", password="Str0ng!Pass123")
        self.other = User.objects.create_user(username="b@x.com", password="Str0ng!Pass123")
        self.client.force_authenticate(self.user)
        self.payload = {"name": "Ravi", "age": 45, "gender": "M"}

    def test_requires_authentication(self):
        self.client.force_authenticate(None)
        res = self.client.get("/api/patients/")
        self.assertEqual(res.status_code, 401)

    def test_create_patient(self):
        res = self.client.post("/api/patients/", self.payload, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Patient.objects.get().created_by, self.user)

    def test_invalid_age(self):
        res = self.client.post(
            "/api/patients/", {**self.payload, "age": 200}, format="json"
        )
        self.assertEqual(res.status_code, 400)

    def test_list_only_own_patients(self):
        Patient.objects.create(created_by=self.user, **self.payload)
        Patient.objects.create(created_by=self.other, **self.payload)
        res = self.client.get("/api/patients/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)

    def test_other_users_patient_returns_404(self):
        patient = Patient.objects.create(created_by=self.other, **self.payload)
        res = self.client.get(f"/api/patients/{patient.id}/")
        self.assertEqual(res.status_code, 404)
