from rest_framework import viewsets
from .models import Applicant  # Import the Applicant model from the current app
from .Serializers import ApplicantSerializer  # Import the ApplicantSerializer from the current app
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class ApplicantViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    
class GetApplicants(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            instance = Applicant.objects.all()
            serializer = ApplicantSerializer(instance, many=True)
            return Response({"msg":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            