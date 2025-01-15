from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import Admin  # Adjust according to your app name
from student.models import SingleParticipant, GroupParticipant, IdeaSubmission
from userauth.models import Investor
from userauth.models import Student
from .serializers import StudentRegistration
from userauth.utils import approval_mail, project_approved, investor_mail_for_approval
from form.models import Applicant
from investor.models import InvestorInterest      


class ApproveInvestors(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            investor_ids = request.data.get("ivestors")
            
            if not isinstance(investor_ids, list) or not investor_ids:
                return Response({"msg": "A list of student IDs is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            investors = Investor.objects.filter(id__in = investor_ids)
            
            if not investors.exists():
                return Response({"msg":"No Investor found for the given id"}, status=status.HTTP_400_BAD_REQUEST)
            
            for investor in investors:
                if investor.is_active == False:
                    return Response({"msg":f"investor with ID: {investor.id} has not been verified"}, status=status.HTTP_400_BAD_REQUEST)
                
                investor.admin_approval = True
                investor.save()
                
                investor_mail_for_approval(investor_mail=investor.email, investor_name=investor.full_name)
                
                return Response({"msg":f"Investor has been approved successfully and mail sent."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        
class ShortListProject(APIView):
    permission_classes = [AllowAny]
    def patch(self, request):
        try:
            students = request.data.get("stud_id")
            
            # Validate input: it should be a non-empty list
            if not isinstance(students, list) or not students:
                return Response({"msg": "A list of student IDs is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Fetch the IdeaSubmission objects for the given student IDs
            ideas = IdeaSubmission.objects.filter(stud_id__in=students)
            
            # Check if any ideas exist for the given student IDs
            if not ideas.exists():
                return Response({"msg": "No idea found for the given student IDs."}, status=status.HTTP_404_NOT_FOUND)

            # Process each idea
            for idea in ideas:
                idea.admin_approval = True
                idea.save()

                # Fetch the student object
                try:
                    student_instance = Student.objects.get(id=idea.stud_id.id)
                except Student.DoesNotExist:
                    continue  # If the student doesn't exist, skip to the next idea

                # Send project approval email
                project_approved(
                    email=student_instance.email,
                    name=student_instance.full_name
                )

            return Response(
                {"msg": "Projects have been accepted."},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
class AllStudents(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            students = Student.objects.filter(is_active=True)
            serializer = StudentRegistration(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentApprovalView(APIView):
    permission_classes = [AllowAny]
    
    def patch(self, request):
        try:
            student_ids = request.data.get("student_id")  # Expecting a list of student IDs
            approval = request.data.get("status")
            
            if not isinstance(student_ids, list) or not student_ids:
                return Response({"msg": "A list of student IDs is required."}, status=status.HTTP_400_BAD_REQUEST)

            if approval not in ["accept", "denied"]:
                return Response({"msg": "Approval can be either 'accept' or 'denied'."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch all students whose IDs are in the list
            students = Student.objects.filter(id__in=student_ids)
            
            if not students.exists():
                return Response({"msg": "No students found for the given IDs."}, status=status.HTTP_404_NOT_FOUND)

            # Process each student
            for student in students:
                if not student.is_active:
                    return Response(
                        {"msg": f"Student {student.id} has not been verified."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Update the approval status
                student.admin_approval = True if approval == "accept" else False
                student.save()

                # Send approval/denial email
                approval_mail(student_email=student.email, stud_name=student.full_name)

            return Response(
                {"msg": f"Students have been {'accepted' if approval == 'accept' else 'denied'}."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # def patch(self, request):
    #     try:
    #         stud_id = request.data.get("student_id")
    #         approval = request.data.get("status")
            
    #         if approval not in ["accept", "denied"]:
    #             return Response({"msg":"Approval can be either 'accept' or 'denied'."}, status=status.HTTP_400_BAD_REQUEST)
                
                
    #         stud_instance = get_object_or_404(Student, id=stud_id)
            
    #         if stud_instance.is_active == False:
    #             return Response("The user has not been verified" , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    #         stud_instance.admin_approval = True if approval == 'accept' else False
    #         stud_instance.save()
            
    #         approval_mail(student_email=stud_instance.email, stud_name=stud_instance.full_name)
            
    #         return Response({"msg":f"The Student has been {'accepted' if approval == 'accept' else 'denied'}"}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({"msg":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class StudentCount(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            count = Student.objects.count()
            verified_count = Student.objects.filter(is_active=False).count()
            return Response({"total_registered_student_count":count, 'verified_student_count':verified_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch admin object
            admin = get_object_or_404(Admin, email=email)

            # Validate password
            if not check_password(password, admin.password):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(admin)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminDashboard(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        single_count = IdeaSubmission.objects.filter(is_single_sub=True).count()

        group_count = IdeaSubmission.objects.filter(is_single_sub=False).count()

        students = Student.objects.count()

        investor_count = Investor.objects.count()

        total_count = single_count + group_count

        ai_ml = IdeaSubmission.objects.filter(project_type='Technology').count() 

        real_estate_count = IdeaSubmission.objects.filter(project_type='Real Estate').count()

        healthcare_biotech_count = IdeaSubmission.objects.filter(project_type='Healthcare and Biotech').count()

        ecommerce_retail_count = IdeaSubmission.objects.filter(project_type='E-commerce and Retail').count()

        education_count = IdeaSubmission.objects.filter(project_type='Education').count()

        finance_fintech_count = IdeaSubmission.objects.filter(project_type='Finance and FinTech').count()

        energy_sustainability_count = IdeaSubmission.objects.filter(project_type='Energy and Sustainability').count()

        entertainment_media_count = IdeaSubmission.objects.filter(project_type='Entertainment and Media').count()

        agriculture_food_count = IdeaSubmission.objects.filter(project_type='Agriculture and Food').count()

        fashion_lifestyle_count = IdeaSubmission.objects.filter(project_type='Fashion and Lifestyle').count()
            
        others_count = IdeaSubmission.objects.filter(project_type='Others').count()
        
        applicants = Applicant.objects.count()
        
        technology = IdeaSubmission.objects.filter(project_type='Technology').count()
        
        pharmacy = IdeaSubmission.objects.filter(project_type='Pharmacy').count()   
        
        interested_investor_count = InvestorInterest.objects.count()

        return Response({
            "single_participant_count": single_count,
            "group_count": group_count,
            "total_count_of_single_and_group_participants": total_count,
            "investor_count": investor_count,
            "total_studens": students,
            "innovate_X_count_of_applicants": applicants,
            "AI/ML": ai_ml,
            "Real Estate": real_estate_count,
            "Healthcare and Biotech": healthcare_biotech_count,
            "E-commerce and Retail": ecommerce_retail_count,
            "Education": education_count,
            "Finance and FinTech": finance_fintech_count,
            "Energy and Sustainability": energy_sustainability_count,
            "Entertainment and Media": entertainment_media_count,
            "Agriculture and Food": agriculture_food_count,
            "Fashion and Lifestyle": fashion_lifestyle_count,
            "Technology": technology,
            "Pharmacy": pharmacy,
            "Others": others_count,
            "interested_investor_count": interested_investor_count
        })
