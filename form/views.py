from rest_framework import viewsets
from .models import Applicant  # Import the Applicant model from the current app
from .Serializers import ApplicantSerializer  # Import the ApplicantSerializer from the current app
from rest_framework.permissions import AllowAny

class ApplicantViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer