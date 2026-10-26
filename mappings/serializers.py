from rest_framework import serializers

from .models import PatientDoctorMapping


class MappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)
    specialization = serializers.CharField(
        source="doctor.specialization", read_only=True
    )

    class Meta:
        model = PatientDoctorMapping
        fields = [
            "id", "patient", "doctor", "patient_name",
            "doctor_name", "specialization", "assigned_at",
        ]
        read_only_fields = ["id", "assigned_at"]

    def validate_patient(self, patient):
        if patient.created_by != self.context["request"].user:
            raise serializers.ValidationError(
                "You can only assign doctors to your own patients."
            )
        return patient