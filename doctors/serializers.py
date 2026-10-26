from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id", "name", "email", "phone", "specialization",
            "experience_years", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_experience_years(self, value):
        if value > 70:
            raise serializers.ValidationError("Enter a valid number of years.")
        return value