from django.conf import settings
from investor.Elephant_aI import evaluate_business_pitch
from userauth.models import Student
from student.models import IdeaSubmission
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from student.serializers import SingleParticipantSerializer, GroupParticipantSerializer, IdeaSubmissionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from student.models import IdeaSubmission, SingleParticipant, GroupParticipant
from rest_framework.permissions import AllowAny
from userauth.utils import send_funding_confirmation_to_investor, send_funding_email_to_student, send_funding_confirmation_to_investor_about_funding, send_funding_success_email_to_student
from userauth.models import Investor
from .serializers import InvestorSerializer
from .models import InvestorFunding, InvestorInterest
from .serializers import InvestorInterestSerializer, InvestorFundingSerializer
from django.utils.timezone import now


class AllApprovedInvestors(APIView):
    def get(self, request):
        try:
            instance = Investor.objects.filter(admin_approval=True)
            serializer = InvestorSerializer(instance, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SendMailFromInvestorToShowInterest(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:

            idea_id = request.data.get('idea_id')
            investor_id = request.data.get('investor_id')
            message = request.data.get('message')

            if not idea_id or not investor_id:
                return Response({"msg": "Investor_id and idea_id must be provided."}, status=status.HTTP_400_BAD_REQUEST)

            instance = IdeaSubmission.objects.select_related(
                'stud_id').get(id=idea_id)

            email = instance.stud_id.email
            name = instance.stud_id.full_name

            investor_instance = get_object_or_404(Investor, id=investor_id)
            investor_name = investor_instance.full_name
            investor_email = investor_instance.email
            investor_linkedIn = investor_instance.linked_url
            
            inve_instance = Investor.objects.get(id=investor_id)

            
            data = InvestorInterest.objects.create(
                datetime = now(),
                idea_id = instance.id,
                investor_id = inve_instance.id
            )
            
            data.save()

            send_funding_success_email_to_student(
                investor_name=investor_name, investor_email=investor_email, stud_name=name, student_email=email, description=message, linkedin_url=investor_linkedIn)

            send_funding_confirmation_to_investor_about_funding(
                investor_name=investor_name, investor_email=investor_email, stud_name=name, student_email=email)

            # instance.status = 'interested'
            instance.save()
            return Response({"msg": "Ivestor and student are notified about the interest of the investor"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from .models import InvestorInterest, InvestorFunding

class SendMailFromInvestorToInvest(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:

            idea_id = request.data.get('idea_id')
            investor_id = request.data.get('investor_id')
            message = request.data.get('message')

            if not idea_id or not investor_id:
                return Response({"msg": "Investor_id and idea_id must be provided."}, status=status.HTTP_400_BAD_REQUEST)

            instance = IdeaSubmission.objects.select_related(
                'stud_id').get(id=idea_id)

            email = instance.stud_id.email
            name = instance.stud_id.full_name

            investor_instance = get_object_or_404(Investor, id=investor_id)
            investor_name = investor_instance.full_name
            investor_email = investor_instance.email
            investor_linkedIn = investor_instance.linked_url
            # instance.status = 'funded'
            instance.save()
            
            # data = InvestorFunding.objects.create(
            #     datetime = now(),
            #     amount = None,
            #     comments=message,
            #     idea_id = 
            # )
                        
            send_funding_email_to_student(
                investor_name=investor_name, investor_email=investor_email, stud_name=name, student_email=email, description=message, linkedin_url=investor_linkedIn)

            send_funding_confirmation_to_investor(
                investor_name=investor_name, investor_email=investor_email, stud_name=name, student_email=email)

            return Response({"msg": "Idea is funded and the student is notified"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetIdeaSubmission(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        instance = IdeaSubmission.objects.all()
        serializer = IdeaSubmissionSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetGroupParticipant(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        instance = GroupParticipant.objects.all()
        serializer = GroupParticipantSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSingleParticipant(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        sig_par = SingleParticipant.objects.all()

        data = [
            {
                "id": participant.id,
                "stud_id": participant.stud_id.id,  # Access the related `Student`'s id
                "stud_name": participant.stud_id.full_name,
                "project_type": participant.project_type,
                "created_at": participant.created_at
            }
            for participant in sig_par
        ]

        return Response({"data": data}, status=status.HTTP_201_CREATED)


class IdeaStatus(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            interested = IdeaSubmission.objects.filter(
                status='interested').count()
            submitted = IdeaSubmission.objects.filter(
                status='submitted').count()
            funded = IdeaSubmission.objects.filter(status='funded').count()

            return Response({
                "interested": interested,
                "submitted": submitted,
                "funded": funded
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            data = IdeaSubmission.objects.values('stud_id', 'title')

            return Response({
                "data": data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, stud_id):
        try:
            # stud_id = request.data.get('stud_id')

            if not stud_id:
                return Response({"error": "stud_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            stud_name = Student.objects.values(
                'full_name').get(id=stud_id)['full_name']
            # idea_data = IdeaSubmission.objects.values('stud_id', 'title','description','idea').get(stud_id=stud_id)
            idea_data = list(IdeaSubmission.objects.values(
                'stud_id', 'title', 'description', 'idea', 'ppt', 'video_file', 'status').filter(stud_id=stud_id))

            sing_par = None
            grp_par = None

            # Handling SingleParticipant query
            sing_par = SingleParticipant.objects.filter(stud_id=stud_id).values(
                'project_type')  # Use filter instead of get
            if sing_par.exists():  # Check if there are results
                sing_par = sing_par[0]  # Take the first record if necessary

            data = {
                "stud_name": stud_name,
                "idea_dat": idea_data,
            }

            if sing_par:  # Only add if there's data
                data["sing_par"] = sing_par

            # Handling GroupParticipant query
            grp_par = GroupParticipant.objects.filter(
                gpr=stud_id).values('name_of_group', 'number_of_member', 'project_type')
            if grp_par.exists():  # Check if there are results
                grp_par = grp_par[0]  # Take the first record if necessary
                data["grp_par"] = grp_par

            return Response({"data": data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def get_full_s3_url(relative_path):
    if relative_path:
        return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{relative_path}"
    return None


class AISummary(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Validate and retrieve the submission ID
            file_id = request.data.get("submission_id")
            if not file_id:
                return JsonResponse({"error": "submission_id is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the IdeaSubmission instance
            instance = get_object_or_404(IdeaSubmission, pk=file_id)

            # Check if the file is a PDF
            file_path = get_full_s3_url(instance.idea)

            if not file_path:
                return Response({"msg": "File path is invalid and file not found."}, status=status.HTTP_400_BAD_REQUEST)

            if not file_path.endswith('.pdf'):
                return JsonResponse({"error": "The file must be a PDF."}, status=status.HTTP_400_BAD_REQUEST)

            # Process the file and get the result
            result = evaluate_business_pitch(file_path)
            
            if result is None:
                return Response(
                    {"error": "Failed to process the file. Please check the PDF and try again."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return JsonResponse(result, safe=False, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class AISummary(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):

#         try:
#             file_id = request.data.get("submission_id")
#             if not file_id:
#                 return Response("submission Id id required.", status=status.HTTP_400_BAD_REQUEST)
#             instance = get_object_or_404(IdeaSubmission, pk=file_id)

#             file_path = instance.idea
#             if not file_path.name.lower().endswith(".pdf"):
#                 return JsonResponse({"error": "The file must be a PDF."}, status=status.HTTP_400_BAD_REQUEST)
#             print(file_path)
#             result = evaluate_business_pitch(file_path)
#             print(result)
#             return JsonResponse({"result": result}, status=200)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)


class ChangeStatus(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, pk=None):
        status = request.data.get('status')

        status_list = ['approved', 'inprogressed',
                       'short_listed', 'submit', 'viewed']

        if status not in status_list:
            return Response({"msg": f"Status must be one of: {', '.join(status_list)}"})

        obj = get_object_or_404(IdeaSubmission, id=pk)

        status_mapping = {
            'approved': 'approved',
            'inprogressed': 'inprogressed',
            'short_listed': 'short_listed',
            'submit': 'submit',
            'viewed': 'viewed',
        }

        # Update the specific status field to True
        setattr(obj, status_mapping[status], True)

        # Save the changes to the database
        obj.save()

        return Response({"message": "Status updated successfully"})

# AI/ML
# Technology
# Real Estate
# Healthcare and Biotech
# E-commerce and Retail
# Education
# Finance and FinTech
# Energy and Sustainability
# Entertainment and Media
# Agriculture and Food
# Fashion and Lifestyle
# Others


class AllProjects(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            instance = IdeaSubmission.objects.all()
            idea_serializer = IdeaSubmissionSerializer(instance, many=True)

            instance = GroupParticipant.objects.all()
            group_serializer = GroupParticipantSerializer(instance, many=True)

            instance = SingleParticipant.objects.all()
            single_serializer = SingleParticipantSerializer(
                instance, many=True)

            return Response({"Idea_Submission": idea_serializer.data,
                            "group_Submission": group_serializer.data,
                             "single_Submission": single_serializer.data
                             })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class InvestorDataAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            investors = Investor.objects.all()
            serializer = InvestorSerializer(investors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
class SelfInvestorData(APIView):
    permission_classes = [AllowAny]

    def get(self, request, inve_id):
        try:
            inv_interest = InvestorInterest.objects.filter(investor_id=inve_id)
            investor_funded = InvestorFunding.objects.filter(investor_id=inve_id)
            
            fund_serializer = InvestorFundingSerializer(investor_funded, many=True)
            interest_serializer = InvestorInterestSerializer(inv_interest, many=True)
            
            return Response({"interested":interest_serializer.data, "funded":fund_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
             
            

