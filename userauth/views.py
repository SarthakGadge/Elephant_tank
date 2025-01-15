from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from userauth.models import Investor
from userauth.Rolepermissoin import IsStudent
import re
from rest_framework.response import Response
from rest_framework import status
from admin_app.models import Admin
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.utils import timezone
import random
from .new_utils import check_and_reply
from django.shortcuts import render
import jwt
from userauth.models import Student
from userauth.serializers import StudentSerializer
# Create your views here.
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from userauth.utils import generate_and_send_otp, mail_after_verifiation
from django.contrib.auth.hashers import make_password
from rest_framework.throttling import ScopedRateThrottle

User = Student

class CustomRegisterThrottle(ScopedRateThrottle):
    THROTTLE_RATES = {
        'register_student': '5/min',  # Define the rate directly in the custom class
    }


class RegisterStudentView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [CustomRegisterThrottle]
    throttle_scope = 'register_student'

    def post(self, request):
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        institution = request.data.get('institution')
        role = request.data.get('role', 'Student')  # Default to 'Student' if not provided
        address = request.data.get('address')
        postal_code = request.data.get('postal_code')
        country = request.data.get('country')
        city = request.data.get('city')
        state = request.data.get('state')
        gender = request.data.get('gender', 'M')  # Default to 'M' if not provided
        field_of_study = request.data.get('field_of_study')
        graduation_year = request.data.get('graduation_year')
        graduation_degree = request.data.get('graduation_degree')
        post_graduation_degree = request.data.get('post_graduation_degree')
        linked_url = request.data.get('linked_url')
        is_group = request.data.get('is_group')
        group_name = request.data.get('group_name')
        group_members = request.data.get('group_members')
        email2 = request.data.get('email2')
        email3 = request.data.get('email3')
        email4 = request.data.get('email4')

        required_fields = [
            "full_name", "email", "password", "phone_number", "role", "institution",
            "address", "postal_code", "country", "city", "state", "gender", "field_of_study", "graduation_year","is_group"
        ]

        for field in required_fields:
            if not request.data.get(field):
                return Response({'msg': f'{field.capitalize()} is required'}, status=status.HTTP_400_BAD_REQUEST)

        if is_group not in ['True', 'False']:
            return Response({'msg': 'is_group must be a boolean value'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not re.match(r'^\d{10}$', phone_number):
            return Response({'msg': 'Invalid phone number. Must be 10 digits.'}, status=status.HTTP_400_BAD_REQUEST)

        if Student.objects.filter(email=email).exists():
            return Response({'msg': 'Email is already in use.'}, status=400)
        
        if Student.objects.filter(phone_number=phone_number).exists():
            return Response({'msg': 'Phone number is already in use.'}, status=400)
        
        if int(group_members) > 4:
            return Response({'msg': 'Group cannot have more than 4 members'}, status=400)

        user = User.objects.create(
            full_name=full_name,
            email=email,
            password=make_password(password),
            phone_number=phone_number,
            institution=institution,
            linked_url=linked_url,
            role=role,
            is_active=False,
            address=address,
            postal_code=postal_code,
            country=country,
            city=city,
            admin_approval=False,
            state=state,
            gender=gender,
            field_of_study=field_of_study,
            graduation_year=graduation_year,
            graduation_degree=graduation_degree,
            post_graduation_degree=post_graduation_degree,
            is_group=is_group,
            group_name=group_name,
            group_members=group_members,
            email2=email2,
            email3=email3,
            email4=email4,
        )
        user.save()

        if check_and_reply(user):
            return Response({'msg': "Verify your email to complete registration. OTP sent for account activation"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg": "Error sending OTP. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User2 = Investor


class RegisterInvestor(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        organisation = request.data.get('organisation')
        gender = request.data.get('gender')
        role = request.data.get('role')
        domain = request.data.get('domain')
        linked_url = request.data.get('linked_url')
        

        required_fields = ['full_name', 'email', 'password',
                           'phone_number', 'organisation', 'role', 'gender', 'domain', 'linked_url']

        for field in required_fields:
            if not request.data.get(field):
                return Response({'msg': f'{field.capitalize()} is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r'^\d{10}$', phone_number):
            return Response({'msg': 'Invalid phone number. Must be 10 digits.'}, status=status.HTTP_400_BAD_REQUEST)

        if Investor.objects.filter(email=email).exists():
            return Response({'msg': 'Email already in use.'}, status=400)

        user = Investor.objects.create(
            full_name=full_name,
            email=email,
            password=make_password(password),
            phone_number=phone_number,
            organisation=organisation,
            gender=gender,
            role=role,
            domain=domain,
            linked_url=linked_url,
            is_active=False
        )
        user.save()

        if generate_and_send_otp(user):
            return Response({'msg': "Verify your email to complete registration. OTP sent for account activation"})
        else:
            return Response({"msg": "Error sending OTP. Please try again later."})


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        role = request.data.get('role')

        if role == 'Student':
            try:
                stud = Student.objects.get(email=email)

                if stud.otp == otp and stud.is_otp_valid():
                    stud.is_active = True
                    stud.otp = None
                    stud.otp_expiry = None
                    stud.max_otp_try = 5
                    stud.otp_max_out = None
                    stud.save()

                    refresh = RefreshToken.for_user(stud)
                    
                    mail_after_verifiation(stud_email=email)
                    
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'role': role
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            except Student.DoesNotExist:
                return Response({'error': 'Student does not exit.'}, status=status.HTTP_404_NOT_FOUND)

        if role == 'Investor':
            try:
                inve = Investor.objects.get(email=email)

                if inve.otp == otp and inve.is_otp_valid():
                    inve.is_active = True
                    inve.otp = None
                    inve.otp_expiry = None
                    inve.max_otp_try = 5
                    inve.otp_max_out = None
                    inve.save()

                    refresh = RefreshToken.for_user(inve)
                    
                    mail_after_verifiation(stud_email=email)
                    
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'role': role
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except Investor.DoesNotExist:
                return Response({'error': 'Investor does not exit.'}, status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = None
        user_type = None

        # Fetch admin object
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
            pass

        # Check if the user is a Student
        try:
            user = Student.objects.get(email=email)
            user_type = "Student"
        except Student.DoesNotExist:
            pass

        # Check if the user is an Investor
        if not user:
            try:
                user = Investor.objects.get(email=email)
                user_type = "Investor"
            except Investor.DoesNotExist:
                return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Verify the password
        if not check_password(password, user.password):
            return Response({"msg": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user is active
        if not user.is_active:
            if user.can_send_otp():
                otp = str(random.randint(1000, 9999))
                user.otp = otp
                user.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
                user.max_otp_try -= 1
                if user.max_otp_try == 0:
                    user.otp_max_out = timezone.now() + timezone.timedelta(hours=1)
                user.save()
                # Assuming `generate_and_send_otp` is implemented
                generate_and_send_otp(user)
                return Response(
                    {"msg": "Your email address has not been verified. An OTP has been sent to your email for account activation"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response({'msg': "Max OTP attempts reached. Try again later."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT tokens for the authenticated user
        
        if user.admin_approval == False:
            return Response({"msg":"This profile has not been approved by the admin"}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.full_name,
            'email': user.email,
            'role': user.role,
            'user_type': user_type,
        }, status=status.HTTP_200_OK)
        
        
from .utils import forgot_pass_mail

class ForgotPassword(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check for user in Student and Investor tables
        user_model = None
        try:
            instance = Student.objects.get(email=email)
            user_model = "Student"
        except Student.DoesNotExist:
            try:
                instance = Investor.objects.get(email=email)
                user_model = "Investor"
            except Investor.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP and set expiry
        otp = str(random.randint(1000, 9999))
        instance.password_reset_otp = otp
        instance.password_reset_otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
        instance.save()

        # Send email
        forgot_pass_mail(mail=email, otp=otp)

        return Response(
            {
                "message": f"Password reset OTP sent to your email. User type: {user_model}"
            },
            status=status.HTTP_200_OK
        )

class ForgotPasswordVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        if not all([email, otp, new_password]):
            return Response({"error": "Email, OTP, and new password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user_model = None
        try:
            # Check if the user exists in Student or Investor models
            instance = Student.objects.get(email=email)
            user_model = "Student"
        except Student.DoesNotExist:
            try:
                instance = Investor.objects.get(email=email)
                user_model = "Investor"
            except Investor.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Validate OTP and expiry
        if instance.password_reset_otp == otp and instance.password_reset_otp_expiry > timezone.now():
            # Reset the password
            instance.password = make_password(new_password)  # Hash the password
            instance.password_reset_otp = None
            instance.password_reset_otp_expiry = None
            instance.save()

            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)


from .utils import resend_otp

class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        
        otp = str(random.randint(1000, 9999))

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Check if the user exists in Student or Investor models
            instance = Student.objects.get(email=email)
            user_model = "Student"
        except Student.DoesNotExist:
            try:
                instance = Investor.objects.get(email=email)
                user_model = "Investor"
            except Investor.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
        
        instance.otp = otp
        instance.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
        instance.max_otp_try -= 1
        if instance.max_otp_try == 0:
            instance.otp_max_out = timezone.now() + timezone.timedelta(hours=1)
        instance.save()

        if instance.is_active == 1:
            return Response({"error": "This account is already active"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            resend_otp(email=email, otp=otp)
            return Response({"msg": "Your email address has not been verified. An OTP has been sent to your email for account activation"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": "Problem while sending OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



        
        
        