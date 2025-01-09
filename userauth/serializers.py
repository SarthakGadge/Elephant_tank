from rest_framework import serializers
from userauth.models import Student, Investor

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['full_name','email','password','phone_number','institution','role']

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ['full_name','email','password','phone_number','role','gender','organisation']

        