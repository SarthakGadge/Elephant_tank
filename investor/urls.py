from django.urls import path
from .views import AllApprovedInvestors, GetGroupParticipant, GetSingleParticipant, GetIdeaSubmission, InvestorDataAPIView, SelfInvestorData, SendMailFromInvestorToInvest, IdeaStatus, ProjectDetail, ProjectDetailView, AISummary, ChangeStatus, AllProjects, SendMailFromInvestorToShowInterest

urlpatterns = [
    path("get_idea_submission/", GetIdeaSubmission.as_view(),
         name="GetIdeaSubmission"),
    path("get_group_participants/",
         GetGroupParticipant.as_view(), name="GetGroupParticipant"),
    path("get_single_participants/",
         GetSingleParticipant.as_view(), name="GetSingleParticipant"),
    path("idea_status_count/", IdeaStatus.as_view(), name="IdeaStatus"),
    #     path("project_detail/", ProjectDetail.as_view(), name="IdeaStatus"),
    path("project_detail_view/<int:stud_id>/",
         ProjectDetailView.as_view(), name="IdeaStatus"),
    path('pdf-summary/', AISummary.as_view(), name='pdf_summary'),
    # path('change_status/<int:pk>/', ChangeStatus.as_view(), name='change_status'),
    path('all_projects/', AllProjects.as_view(), name='change_status'),
    path('fund_project/', SendMailFromInvestorToInvest.as_view(),
         name='SendMailFromInvestorToInvest'),
    path('show_interest/', SendMailFromInvestorToShowInterest.as_view(),
         name='SendMailFromInvestorToInvest'),
    path('investor_data/', InvestorDataAPIView.as_view(),
         name='SendMailFromInvestorToInvest'),
    path('approved_investors/', AllApprovedInvestors.as_view(),
         name='SendMailFromInvestorToInvest'),
    path("self_investor/<int:inve_id>/", SelfInvestorData.as_view(), name='SelfInvestorData')

]
