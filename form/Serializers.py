from django.forms import ValidationError
from rest_framework import serializers
from .models import Applicant  

class ApplicantSerializer(serializers.ModelSerializer):
    # confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Applicant
        fields = '__all__'

def validate_resume_upload(self, value):
        if value.size > 5 * 1024 * 1024:  # Limit file size to 5MB
            raise serializers.ValidationError("The file size exceeds the 5MB limit.")
        return value