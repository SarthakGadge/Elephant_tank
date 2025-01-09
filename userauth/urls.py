from django.urls import path
from userauth.views import RegisterStudentView, RegisterInvestor,VerifyOTPView,LoginView, ForgotPassword, ForgotPasswordVerifyView, ResendOTPView


urlpatterns = [
    path('register_stud/', RegisterStudentView.as_view(), name='register'),
    path('register_inve/', RegisterInvestor.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot_password/', ForgotPassword.as_view(), name='login'),
    path('reset_password/', ForgotPasswordVerifyView.as_view(), name='login'),
    path('resend_otp/', ResendOTPView.as_view(), name='login'),
    
    
]