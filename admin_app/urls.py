from django.urls import path
from .views import AdminLoginView, AdminDashboard, AllStudents, StudentApprovalView, StudentCount, ShortListProject, ApproveInvestors

urlpatterns = [
    # path("admin_login/", AdminLoginView.as_view(), name='admin_login'),
    path("admin_dashboard/", AdminDashboard.as_view(), name='admin_login'),
    path('verified_students/', AllStudents.as_view(), name='all_students'),
    path('students_approval/', StudentApprovalView.as_view(), name='student_approval'),
    path('students_count/', StudentCount.as_view(), name='student_count'),
    path('approve_project/', ShortListProject.as_view(), name='ShortListProject'),
    path('approve_investor/', ApproveInvestors.as_view(), name='ShortListProject'),
]

