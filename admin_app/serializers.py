from rest_framework.serializers import ModelSerializer
from userauth.models import Student

class StudentRegistration(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'