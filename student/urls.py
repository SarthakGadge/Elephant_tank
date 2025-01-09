from django.urls import path
from .views import GetGroupParticipantAndIdeas, ProjectInfoUpd, ShowMyInterestedInvestors, SingleParticipantView, IdeaSubmissionView, GetAllProjectInfo, GetSingleParticipantAndIdeas, GetStudentProjectInfo, GetStudentGroupAndIdeas, GetGroupRequest, AllGroups,  GroupParticipantView, IdeaSubmissionStatus, JoinGroupView, CreateGroupView, UpdateMembershipRequestStatusView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("single_participant/", SingleParticipantView.as_view(),
         name="single-participant"),
    path("group_participant/", GroupParticipantView.as_view(),
         name="group_participant"),
    path("idea_submission/", IdeaSubmissionView.as_view(), name="idea_submission"),
    path("idea_submission_status/",
         IdeaSubmissionStatus.as_view(), name="idea_submission"),
    path('create-group/', CreateGroupView.as_view(), name='create-group'),
    path('join-group/', JoinGroupView.as_view(), name='join-group'),
    path('update-membership-request/<int:request_id>/',
         UpdateMembershipRequestStatusView.as_view(),
         name='update-membership-request'),
    path('all_groups/', AllGroups.as_view(),
         name='SendMailFromInvestorToInvest'),
    path('all_project_details/', GetAllProjectInfo.as_view(),
         name='SendMailFromInvestorToInvest'),
    path('all_project_details_for_grp/', GetStudentGroupAndIdeas.as_view(),
         name='SendMailFromInvestorToInvest'),
    path('group_notification/', GetGroupRequest.as_view(),
         name='SendMailFromInvestorToInvest'),
    path('project_info/', ProjectInfoUpd.as_view(),
         name='SendMailFromInvestorToInvest'),
    path('all_single_participants/', GetSingleParticipantAndIdeas.as_view(),
         name='SendMailFromInvestorToInvest'),
    path('all_group_participants/', GetGroupParticipantAndIdeas.as_view(),
         name='SendMailFromInvestorToInvest'),
    path('interested_investors/<int:stud_id>/', ShowMyInterestedInvestors.as_view(),
         name='ShowMyInterestedInvestors'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
