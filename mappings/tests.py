from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from doctors.models import Doctor
from patients.models import Patient

from .models import PatientDoctorMapping


class MappingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="a@x.com", password="Str0ng!Pass123")
        self.other = User.objects.create_user(username="b@x.com", password="Str0ng!Pass123")
        self.patient = Patient.objects.create(
            created_by=self.user, name="Ravi", age=45, gender="M"
        )
        self.doctor = Doctor.objects.create(
            created_by=self.user, name="Meera", email="m@h.com", specialization="Cardiology"
        )
        self.client.force_authenticate(self.user)

    def test_assign_doctor(self):
        res = self.client.post(
            "/api/mappings/",
            {"patient": self.patient.id, "doctor": self.doctor.id},
            format="json",
        )
        self.assertEqual(res.status_code, 201)

    def test_duplicate_mapping_rejected(self):
        data = {"patient": self.patient.id, "doctor": self.doctor.id}
        self.client.post("/api/mappings/", data, format="json")
        res = self.client.post("/api/mappings/", data, format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_assign_to_other_users_patient(self):
        self.client.force_authenticate(self.other)
        res = self.client.post(
            "/api/mappings/",
            {"patient": self.patient.id, "doctor": self.doctor.id},
            format="json",
        )
        self.assertEqual(res.status_code, 400)

    def test_doctors_for_patient(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        res = self.client.get(f"/api/mappings/{self.patient.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)

    def test_delete_mapping(self):
        mapping = PatientDoctorMapping.objects.create(
            patient=self.patient, doctor=self.doctor
        )
        res = self.client.delete(f"/api/mappings/{mapping.id}/")
        self.assertEqual(res.status_code, 204)
        self.assertFalse(PatientDoctorMapping.objects.exists())