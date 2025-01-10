from django.conf import settings
from django.db import connection
from django.shortcuts import render
from investor.models import InvestorInterest
from student.models import SingleParticipant, GroupParticipant, IdeaSubmission
from student.serializers import SingleParticipantSerializer, IdeaSubmissionSerializer
from rest_framework.views import APIView
from userauth.Rolepermissoin import IsStudent
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from userauth.models import Student
from investor.Elephant_aI import evaluate_business_pitch
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from userauth.models import Student, Investor
from student.models import SingleParticipant, GroupParticipant, IdeaSubmission
import random
from .models import Group
from .serializers import GroupSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .models import Group, GroupMembershipRequest
from .serializers import GroupMembershipRequestSerializer, InvestorForStudentSerailizer


class ShowMyInterestedInvestors(APIView):
    permission_classes = [AllowAny]
    def get(self, request, stud_id):
        try:
            stud = IdeaSubmission.objects.get(stud_id=stud_id)
            investors = InvestorInterest.objects.filter(idea_id = stud.id)
            serializer = InvestorForStudentSerailizer(investors, many=True)
            return Response({"msg":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        


class ProjectInfoUpd(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            stud_id = request.query_params.get("stud_id")

            if not stud_id:
                return Response({"error": "stud_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            stud_instance = Student.objects.get(id=stud_id)
            
            student_data = {
                "id": stud_instance.id,
                "full_name": stud_instance.full_name,
                "email": stud_instance.email,
                "phone_number": stud_instance.phone_number,
                "role": stud_instance.role,
                "institution": stud_instance.institution,
                "address": stud_instance.address,
                "postal_code": stud_instance.postal_code,
                "country": stud_instance.country,
                "date_of_birth": stud_instance.date_of_birth,
                "city": stud_instance.city,
                "state": stud_instance.state,
                "gender": stud_instance.gender,
                "field_of_study": stud_instance.field_of_study,
                "graduation_year": stud_instance.graduation_year
            }
            
            idea_instance = IdeaSubmission.objects.get(stud_id=stud_id)
            
            idea_data = {
                "id": idea_instance.id,
                "title": idea_instance.title if idea_instance.title is not None else None,
                "description": idea_instance.description if idea_instance.description is not None else None,
                "status": idea_instance.status if idea_instance.status is not None else None,
                "idea": idea_instance.idea.url if idea_instance.idea and hasattr(idea_instance.idea, "url") else None,
                "ppt": idea_instance.ppt.url if idea_instance.ppt and hasattr(idea_instance.ppt, "url") else None,
                "video_file": idea_instance.video_file.url if idea_instance.video_file and hasattr(idea_instance.video_file, "url") else None,
                "created_at": idea_instance.created_at if idea_instance.created_at is not None else None,
                "ai_score": idea_instance.ai_score if idea_instance.ai_score is not None else None,
                "stud_id_id": idea_instance.stud_id_id if idea_instance.stud_id_id is not None else None,
                "name_of_group": idea_instance.name_of_group if idea_instance.name_of_group is not None else None,
                "number_of_member": idea_instance.number_of_member if idea_instance.number_of_member is not None else None,
                "project_type": idea_instance.project_type if idea_instance.project_type is not None else None,
                "admin_approval":idea_instance.admin_approval
                
            }

            return Response({"student_data": student_data, "idea_data":idea_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
     
    





class ProjectInfo(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        stud_id = request.query_params.get("stud_id")

        if not stud_id:
            return Response({"error": "stud_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch student instance
            student_instance = get_object_or_404(Student, id=stud_id)

            is_group = student_instance.is_group
            is_leader = student_instance.is_group_leader

            # --- FLOW 1: If student is a group participant ---
            if is_group:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT
                            g.id AS group_id,
                            g.group_name,
                            g.description,
                            g.is_open_for_joining,
                            g.created_at,
                            gmr.id AS membership_request_id,
                            gmr.status AS membership_status,
                            gmr.requested_at,
                            gmr.updated_at,
                            isub.id AS idea_submission_id,
                            isub.title,
                            isub.description AS idea_description,
                            isub.status AS idea_status,
                            isub.idea,
                            isub.ppt,
                            isub.video_file,
                            isub.created_at AS idea_created_at,
                            isub.ai_score
                        FROM
                            student_group g
                        LEFT JOIN
                            student_groupmembershiprequest gmr ON g.id = gmr.group_id
                        LEFT JOIN
                            student_ideasubmission isub ON g.id = isub.group_id
                        WHERE
                            gmr.student_id = %s;
                    """, [stud_id])

                    results = cursor.fetchall()

                # Format results
                group_data = [
                    {
                        "group_id": row[0],
                        "group_name": row[1],
                        "description": row[2],
                        "is_open_for_joining": row[3],
                        "created_at": row[4],
                        "membership_request": {
                            "id": row[5],
                            "status": row[6],
                            "requested_at": row[7],
                            "updated_at": row[8],
                        } if row[5] else None,
                        "idea_submission": {
                            "id": row[9],
                            "title": row[10],
                            "description": row[11],
                            "status": row[12],
                            "idea": row[13],
                            "ppt": row[14],
                            "video_file": row[15],
                            "created_at": row[16],
                            "ai_score": row[17],
                        } if row[9] else None,
                    } for row in results
                ]

                return Response({"flow": "group_participant", "data": group_data}, status=status.HTTP_200_OK)

            # --- FLOW 2: If student is a group leader ---
            elif is_leader:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT
                            g.id AS group_id,
                            g.group_name,
                            g.description,
                            g.is_open_for_joining,
                            g.created_at,
                            isub.id AS idea_submission_id,
                            isub.title,
                            isub.description,
                            isub.status,
                            isub.idea,
                            isub.ppt,
                            isub.video_file,
                            isub.created_at AS idea_created_at,
                            isub.ai_score
                        FROM
                            student_group g
                        LEFT JOIN
                            student_ideasubmission isub ON g.id = isub.group_id
                        WHERE
                            g.created_by_id = %s
                    """, [stud_id])

                    results = cursor.fetchall()

                # Format results
                leader_data = [
                    {
                        "group_id": row[0],
                        "group_name": row[1],
                        "description": row[2],
                        "is_open_for_joining": row[3],
                        "created_at": row[4],
                        "idea_submissions": {
                            "id": row[5],
                            "title": row[6],
                            "description": row[7],
                            "status": row[8],
                            "idea_file": row[9],
                            "ppt_file": row[10],
                            "video_file": row[11],
                            "created_at": row[12],
                            "ai_score": row[13],
                        } if row[5] else None
                    } for row in results
                ]

                return Response({"flow": "group_leader", "data": leader_data}, status=status.HTTP_200_OK)

            # --- FLOW 3: If student is a single participant ---
            else:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT
                            sp.id AS single_participant_id,
                            sp.project_type,
                            sp.created_at,
                            isub.id AS idea_submission_id,
                            isub.title,
                            isub.description,
                            isub.status,
                            isub.idea,
                            isub.ppt,
                            isub.video_file,
                            isub.created_at AS idea_created_at
                        FROM
                            student_singleparticipant sp
                        LEFT JOIN
                            student_ideasubmission isub ON sp.stud_id_id = isub.stud_id_id
                        WHERE
                            sp.stud_id_id = %s
                    """, [stud_id])

                    results = cursor.fetchall()

                # Format results
                single_data = [
                    {
                        "single_participant_id": row[0],
                        "project_type": row[1],
                        "created_at": row[2],
                        "idea_submissions": {
                            "id": row[3],
                            "title": row[4],
                            "description": row[5],
                            "status": row[6],
                            "idea_file": row[7],
                            "ppt_file": row[8],
                            "video_file": row[9],
                            "created_at": row[10],
                        } if row[3] else None
                    } for row in results
                ]

                return Response({"flow": "single_participant", "data": single_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AllGroups(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            group = Group.objects.all()
            group_s = GroupSerializer(group, many=True)
            return Response(group_s.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetGroupRequest(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            group = GroupMembershipRequest.objects.all()
            group_s = GroupMembershipRequestSerializer(group, many=True)
            return Response(group_s.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateMembershipRequestStatusView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, request_id):
        try:
            # Data from request
            action = request.data.get('action')  # 'Accept' or 'Reject'

            # Validate input
            if not action or action not in ['Accept', 'Reject']:
                return Response({"error": "Invalid action. Use 'Accept' or 'Reject'."}, status=status.HTTP_400_BAD_REQUEST)

            # Get the membership request
            membership_request = get_object_or_404(
                GroupMembershipRequest, id=request_id)
            student_instance = get_object_or_404(
                Student, id=membership_request.student_id)
            if action == 'Accept':
                student_instance.is_group = True
                student_instance.save()

            # Check if the logged-in user is the creator of the group
            # if membership_request.group.created_by != request.user:
            #     return Response({"error": "You are not authorized to update this request."}, status=status.HTTP_403_FORBIDDEN)

            # Update the request status
            membership_request.status = 'Accepted' if action == 'Accept' else 'Rejected'
            membership_request.save()

            return Response({"message": f"Request has been {membership_request.status.lower()}."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JoinGroupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:

            # Assuming `request.user` contains the logged-in student instance
            student = request.data.get('stud_id')

            student_instance = get_object_or_404(Student, id=student)

            # Data from request
            group_id = request.data.get('group_id')

            # Validate input
            if not group_id:
                return Response({"error": "Group ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the group exists
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

            # Check if the group is open for joining
            if not group.is_open_for_joining:
                return Response({"error": "This group is not accepting new members."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the student already requested to join this group
            if GroupMembershipRequest.objects.filter(group=group, student=student).exists():
                return Response({"error": "You have already requested to join this group."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the membership request
            membership_request = GroupMembershipRequest.objects.create(
                group=group,
                student=student_instance,
                status='Pending'
            )

            # Serialize the response
            serializer = GroupMembershipRequestSerializer(membership_request)
            return Response({"message": "Join request sent successfully.", "membership_request": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateGroupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Assuming `request.user` contains the logged-in student instance
            student = request.data.get('stud_id')

            student_instance = get_object_or_404(Student, id=student)
            student_instance.is_group_leader = True
            student_instance.save()

            # Data from request
            group_name = request.data.get('group_name')
            description = request.data.get('description', '')
            is_open_for_joining = request.data.get('is_open_for_joining', True)

            # Validate the group name
            if not group_name:
                return Response({"error": "Group name is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the group name is unique
            if Group.objects.filter(group_name=group_name).exists():
                return Response({"error": "Group name already exists."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the group
            group = Group.objects.create(
                group_name=group_name,
                created_by=student_instance,
                description=description,
                is_open_for_joining=is_open_for_joining
            )

            # Serialize the response
            serializer = GroupSerializer(group)
            return Response({"message": "Group created successfully.", "group": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleParticipantView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # print(request.headers)
        try:
            stud_id = request.POST.get('stud_id')

            if not stud_id:
                return Response({"error": "stud_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            if IdeaSubmission.objects.filter(stud_id=stud_id).exists():
                return Response({"error": "Student already submitted one idea."}, status=status.HTTP_400_BAD_REQUEST)

            project_type = request.POST.get('project_type')
            title = request.POST.get('title')
            description = request.POST.get('description')
            idea = request.FILES.get('pdf_files')
            ppt = request.FILES.get('ppt_files')
            video_file = request.FILES.get('video_files')

            if not stud_id or not project_type or not title or not description or not idea:
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                student = Student.objects.get(id=stud_id)
            except Student.DoesNotExist:
                return Response({"error": "Student does not exist"}, status=status.HTTP_404_NOT_FOUND)

            # sing_per = SingleParticipant.objects.create(
            #     stud_id=student,
                
            # )
            
            result = evaluate_business_pitch(idea)
            print(result)
            
            score = result
            
            idea = IdeaSubmission.objects.create(
                project_type=project_type,
                stud_id=student,
                title=title,
                description=description,
                ai_score=score,
                idea=idea,
                ppt=ppt,
                video_file=video_file,
                is_single_sub=True
            )

            # sing_per.save()
            idea.save()

            response_data = {
                "msg": "Idea submitted successfully",
                "stud_id": student.id,
                "project_type": project_type,
                "title": idea.title,
                "description": idea.description,
                "idea": idea.idea.url if idea.idea else None,
                "ppt": idea.ppt.url if idea.ppt else None,
                "video_file": idea.video_file.url if idea.video_file else None,
                "ai_score": score
            }

            return Response({"msg": "Idea submitted successfully", 'response_data': response_data}, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist as e:
            return Response({"error": f"Object does not exist: {str(e)}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GroupParticipantView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:

            stud = request.data.get('stud_id')

            if not stud:
                return Response({"error": "stud_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            if IdeaSubmission.objects.filter(stud_id=stud).exists():
                return Response({"error": "group already submitted one idea."}, status=status.HTTP_400_BAD_REQUEST)

            name_of_group = request.data.get('name_of_group')
            number_of_member = request.data.get('number_of_member')
            project_type = request.data.get('project_type')
            title = request.data.get('title')
            description = request.POST.get('description')
            idea = request.FILES.get('pdf_files')
            ppt = request.FILES.get('ppt_files')
            video_file = request.FILES.get('video_files')

            # required_fields = ['stud_id', 'name_of_group',
            #                    'number_of_member', 'project_type']

            # for field in required_fields:
            #     if not request.data.get(field):
            #         return Response({'msg': f'{field.capitalize()} is required'}, status=status.HTTP_400_BAD_REQUEST)

            if not stud or not name_of_group or not project_type or not description or not title or not idea:
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            # try:
            #     grp = Group.objects.get(id=grp_id)
            # except Group.DoesNotExist:
            #     return Response({"error": "Student does not exist"}, status=status.HTTP_404_NOT_FOUND)

            instance = get_object_or_404(Student, id=stud)

            # grp_per = GroupParticipant.objects.create(
            #     stud_id=instance,
            #     name_of_group=name_of_group,
            #     number_of_member=number_of_member,
            #     project_type=project_type
            # )

            idea = IdeaSubmission.objects.create(
                stud_id=instance,
                title=title,
                description=description,
                name_of_group=name_of_group,
                number_of_member=number_of_member,
                idea=idea,
                ppt=ppt,
                video_file=video_file,
                is_single_sub=True,
                project_type=project_type
                )

            # grp_per.save()
            idea.save()

            response_data = {
                "msg": "Group participant record created successfully.",
                "stud_id": instance.id,
                "name_of_group": name_of_group,
                "number_of_member": number_of_member,
                "project_type": project_type,
                "title": idea.title,
                "description": idea.description,
                "idea": idea.idea.url if idea.idea else None,
                "ppt": idea.ppt.url if idea.ppt else None,
                "video_file": idea.video_file.url if idea.video_file else None
            }

            return Response({"msg": "Group participant record created successfully.", "Data": response_data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class IdeaSubmissionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            stud_id = request.POST.get('stud_id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            idea = request.FILES.get('idea')

            required_fields = ['stud_id', 'title', 'description', 'idea']

            try:
                student = Student.objects.get(id=stud_id)
            except Student.DoesNotExist:
                return Response({'msg': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

            valid_file_types = ['application/pdf', 'application/msword',
                                'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'image/jpeg', 'image/png']
            if idea.content_type not in valid_file_types:
                return Response({'msg': 'Invalid file type. Only documents and images are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

            ida_sub = IdeaSubmission.objects.create(
                stud_id=student,
                title=title,
                description=description,
                idea=idea,
                submit=True
            )
            ida_sub.save()

            return Response({"msg": "Idea submitted successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class IdeaSubmissionStatus(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        idea_id = request.GET.get('id')
        if not idea_id:
            return Response({'error': 'ID is required in query parameters'}, status=400)

        try:
            # Fetch the record with the given ID
            idea_submission = get_object_or_404(
                IdeaSubmission, stud_id_id=idea_id)
            serializer = IdeaSubmissionSerializer(idea_submission)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError:
            return Response({'error': 'Invalid ID format'}, status=400)


class GetAllProjectInfo(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        stud_id = request.query_params.get('stud_id')

        if not stud_id:
            return Response({"error": "stud_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        us.id AS student_id,
                        us.full_name,
                        us.email,
                        us.password,
                        sp.project_type,
                        sp.created_at AS single_participant_created_at,
                        isub.id AS idea_submission_id,
                        isub.title AS idea_title,
                        isub.description AS idea_description,
                        isub.created_at AS idea_submission_created_at,
                        isub.idea AS idea_file,
                        isub.video_file,
                        isub.ppt,
                        isub.status AS idea_status,
                        isub.group_id_id AS idea_group_id
                    FROM 
                        userauth_student us
                    LEFT JOIN 
                        student_singleparticipant sp ON us.id = sp.stud_id_id
                    LEFT JOIN 
                        student_ideasubmission isub ON us.id = isub.stud_id_id
                    WHERE 
                        us.id = %s;
                """, [stud_id])
                result = cursor.fetchall()

            # If no result is found, return an error
            if not result:
                return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

            # Prepare the result data
            data = {
                "userauth_student": {
                    "student_id": result[0][0],
                    "full_name": result[0][1],
                    "email": result[0][2],
                    "password": result[0][3]
                },
                "student_singleparticipant": [
                    {
                        "project_type": item[4],
                        "created_at": item[5]
                    } for item in result if item[4] is not None
                ],
                "student_ideasubmission": [
                    {
                        "idea_submission_id": item[6],
                        "title": item[7],
                        "description": item[8],
                        "created_at": item[9],
                        "idea_file": item[10],
                        "video_file": item[11],
                        "ppt": item[12],
                        "idea_status": item[13],
                        "idea_group_id": item[14]
                    } for item in result if item[6] is not None
                ]
            }

            return Response({"data": data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetStudentGroupAndIdeas(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        student_id = request.query_params.get('student_id')

        if not student_id:
            return Response({"error": "student_id is required"}, status=400)

        try:
            # Step 1: Retrieve all GroupMembershipRequest records for the given student_id
            membership_requests = GroupMembershipRequest.objects.filter(
                student__id=student_id)

            # Step 2: Iterate and gather relevant data
            results = []

            for request_item in membership_requests:
                student = request_item.student  # Fetch basic student info
                group = request_item.group  # Group related to membership request

                # Step 3: Fetch GroupParticipant info based on group_id
                group_participant = GroupParticipant.objects.filter(
                    group_id=group).first()

                # Step 4: Fetch all IdeaSubmission entries related to the group
                idea_submissions = IdeaSubmission.objects.filter(
                    group_id=group)

                # Prepare final result for the current membership request
                result_entry = {
                    "student_info": {
                        "id": student.id,
                        "full_name": student.full_name,
                        "email": student.email,
                        "institution": student.institution,
                    },
                    "group_info": {
                        "name_of_group": group_participant.name_of_group if group_participant else None,
                        "number_of_members": group_participant.number_of_member if group_participant else None,
                        "project_type": group_participant.project_type if group_participant else None,
                        "created_at": group_participant.created_at if group_participant else None,
                    },
                    "idea_submissions": [
                        {
                            "id": idea.id,
                            "title": idea.title,
                            "description": idea.description,
                            "status": idea.status,
                            "idea_file": idea.idea.url if idea.idea else None,
                            "ppt_file": idea.ppt.url if idea.ppt else None,
                            "video_file": idea.video_file.url if idea.video_file else None,
                            "created_at": idea.created_at,
                        }
                        for idea in idea_submissions
                    ]
                }

                results.append(result_entry)

            return Response({"data": results}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


# class GetStudentProjectInfo(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         student_id = request.query_params.get('student_id')

#         if not student_id:
#             return Response({"error": "student_id is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # --- FLOW 1: Attempt to fetch data using raw SQL ---
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT
#                         us.id AS student_id,
#                         us.full_name,
#                         us.email,
#                         us.password,
#                         sp.project_type,
#                         sp.created_at AS single_participant_created_at,
#                         isub.id AS idea_submission_id,
#                         isub.title AS idea_title,
#                         isub.description AS idea_description,
#                         isub.created_at AS idea_submission_created_at,
#                         isub.idea AS idea_file,
#                         isub.video_file,
#                         isub.ppt,
#                         isub.status AS idea_status,
#                         isub.group_id_id AS idea_group_id
#                     FROM
#                         userauth_student us
#                     LEFT JOIN
#                         student_singleparticipant sp ON us.id = sp.stud_id_id
#                     LEFT JOIN
#                         student_ideasubmission isub ON us.id = isub.stud_id_id
#                     WHERE
#                         us.id = %s;
#                 """, [student_id])
#                 result = cursor.fetchall()

#             # If data exists in Flow 1, format and return it
#             if result:
#                 data = {
#                     "userauth_student": {
#                         "student_id": result[0][0],
#                         "full_name": result[0][1],
#                         "email": result[0][2],
#                         "password": result[0][3]
#                     },
#                     "student_singleparticipant": [
#                         {
#                             "project_type": item[4],
#                             "created_at": item[5]
#                         } for item in result if item[4] is not None
#                     ],
#                     "student_ideasubmission": [
#                         {
#                             "idea_submission_id": item[6],
#                             "title": item[7],
#                             "description": item[8],
#                             "created_at": item[9],
#                             "idea_file": item[10],
#                             "video_file": item[11],
#                             "ppt": item[12],
#                             "idea_status": item[13],
#                             "idea_group_id": item[14]
#                         } for item in result if item[6] is not None
#                     ]
#                 }
#                 return Response({"data": data, "flow": "flow_1"}, status=status.HTTP_200_OK)

#             # --- FLOW 2: If Flow 1 has no data, proceed with ORM query ---
#             membership_requests = GroupMembershipRequest.objects.filter(
#                 student__id=student_id
#             )

#             if not membership_requests.exists():
#                 return Response({"error": "No data found for the given student_id"}, status=status.HTTP_404_NOT_FOUND)

#             # Collect data for Flow 2
#             results = []

#             for request_item in membership_requests:
#                 student = request_item.student
#                 group = request_item.group

#                 group_participant = GroupParticipant.objects.filter(
#                     group_id=group).first()

#                 idea_submissions = IdeaSubmission.objects.filter(
#                     group_id=group
#                 )

#                 result_entry = {
#                     "student_info": {
#                         "id": student.id,
#                         "full_name": student.full_name,
#                         "email": student.email,
#                         "institution": student.institution,
#                     },
#                     "group_info": {
#                         "name_of_group": group_participant.name_of_group if group_participant else None,
#                         "number_of_members": group_participant.number_of_member if group_participant else None,
#                         "project_type": group_participant.project_type if group_participant else None,
#                         "created_at": group_participant.created_at if group_participant else None,
#                     },
#                     "idea_submissions": [
#                         {
#                             "id": idea.id,
#                             "title": idea.title,
#                             "description": idea.description,
#                             "status": idea.status,
#                             "idea_file": idea.idea.url if idea.idea else None,
#                             "ppt_file": idea.ppt.url if idea.ppt else None,
#                             "video_file": idea.video_file.url if idea.video_file else None,
#                             "created_at": idea.created_at,
#                         }
#                         for idea in idea_submissions
#                     ]
#                 }

#                 results.append(result_entry)

#             return Response({"data": results, "flow": "flow_2"}, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_full_s3_url(relative_path):
    if relative_path:
        return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{relative_path}"
    return None


class GetSingleParticipantAndIdeas(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Fetch all student, single participant, and idea submission data using raw SQL query
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        sp.id AS single_participant_id,
                        sp.stud_id_id AS student_id,
                        sp.project_type,
                        sp.created_at AS single_participant_created_at,
                        isub.id AS idea_submission_id,
                        isub.title AS idea_title,
                        isub.description AS idea_description,
                        isub.status AS idea_status,
                        isub.idea AS idea_file,
                        isub.ppt AS ppt_file,
                        isub.video_file,
                        isub.created_at AS idea_submission_created_at
                    FROM 
                        student_singleparticipant sp
                    LEFT JOIN 
                        student_ideasubmission isub ON sp.stud_id_id = isub.stud_id_id;
                """)
                result = cursor.fetchall()

            # Format the fetched data
            student_data = []
            for row in result:
                student_entry = {
                    "single_participant": {
                        "id": row[0],
                        "student_id": row[1],
                        "project_type": row[2],
                        "created_at": row[3],
                    },
                    "idea_submission": {
                        "idea_submission_id": row[4],
                        "title": row[5],
                        "description": row[6],
                        "status": row[7],
                        # Full S3 URL for idea_file
                        "idea_file": get_full_s3_url(row[8]),
                        # Full S3 URL for ppt_file
                        "ppt_file": get_full_s3_url(row[9]),
                        # Full S3 URL for video_file
                        "video_file": get_full_s3_url(row[10]),
                        "created_at": row[11],
                    }
                }
                student_data.append(student_entry)

            # Return the formatted response
            return Response(
                {"data": student_data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetGroupParticipantAndIdeas(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Fetch all GroupParticipant records and IdeaSubmission records using raw SQL query
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        gp.id AS group_participant_id,
                        gp.group_id AS group_id,
                        gp.name_of_group,
                        gp.number_of_member,
                        gp.project_type AS group_project_type,
                        gp.created_at AS group_created_at,
                        isub.id AS idea_submission_id,
                        isub.title AS idea_title,
                        isub.description AS idea_description,
                        isub.status AS idea_status,
                        isub.idea AS idea_file,
                        isub.ppt AS ppt_file,
                        isub.video_file,
                        isub.created_at AS idea_submission_created_at
                    FROM 
                        student_groupparticipant gp
                    LEFT JOIN 
                        student_ideasubmission isub ON gp.group_id = isub.group_id;
                """)
                result = cursor.fetchall()

            # Format the fetched data
            group_data = []
            for row in result:
                group_entry = {
                    "group_participant": {
                        "id": row[0],
                        "group_id": row[1],
                        "name_of_group": row[2],
                        "number_of_member": row[3],
                        "project_type": row[4],
                        "created_at": row[5],
                    },
                    "idea_submission": {
                        "idea_submission_id": row[6],
                        "title": row[7],
                        "description": row[8],
                        "status": row[9],
                        "idea_file": row[10],
                        "ppt_file": row[11],
                        "video_file": row[12],
                        "created_at": row[13],
                    }
                }
                group_data.append(group_entry)

            # Return the formatted response
            return Response(
                {"data": group_data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetStudentProjectInfo(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        student_id = request.query_params.get('student_id')

        if not student_id:
            return Response({"error": "student_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # --- Iterative Flow Logic ---
            flow = 'flow_1'
            while True:
                if flow == 'flow_1':
                    # --- FLOW 1: Attempt to fetch data using raw SQL ---
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            SELECT 
                                us.id AS student_id,
                                us.full_name,
                                us.email,
                                us.password,
                                sp.project_type,
                                sp.created_at AS single_participant_created_at,
                                isub.id AS idea_submission_id,
                                isub.title AS idea_title,
                                isub.description AS idea_description,
                                isub.created_at AS idea_submission_created_at,
                                isub.idea AS idea_file,
                                isub.video_file,
                                isub.ppt,
                                isub.status AS idea_status,
                                isub.group_id_id AS idea_group_id
                            FROM 
                                userauth_student us
                            LEFT JOIN 
                                student_singleparticipant sp ON us.id = sp.stud_id_id
                            LEFT JOIN 
                                student_ideasubmission isub ON us.id = isub.stud_id_id
                            WHERE 
                                us.id = %s;
                        """, [student_id])
                        result = cursor.fetchall()

                    if result:  # If Flow 1 has data, return that data
                        data = {
                            "userauth_student": {
                                "student_id": result[0][0],
                                "full_name": result[0][1],
                                "email": result[0][2],
                                "password": result[0][3]
                            },
                            "student_singleparticipant": [
                                {
                                    "project_type": item[4],
                                    "created_at": item[5]
                                } for item in result if item[4] is not None
                            ],
                            "student_ideasubmission": [
                                {
                                    "idea_submission_id": item[6],
                                    "title": item[7],
                                    "description": item[8],
                                    "created_at": item[9],
                                    "idea_file": item[10],
                                    "video_file": item[11],
                                    "ppt": item[12],
                                    "idea_status": item[13],
                                    "idea_group_id": item[14]
                                } for item in result if item[6] is not None
                            ]
                        }
                        # If both lists are empty, move to Flow 2
                        if not data["student_singleparticipant"] and not data["student_ideasubmission"]:
                            flow = 'flow_2'
                        else:
                            return Response({"data": data, "flow": "flow_1"}, status=status.HTTP_200_OK)

                elif flow == 'flow_2':
                    # --- FLOW 2: If Flow 1 has no data, check ORM query ---
                    membership_requests = GroupMembershipRequest.objects.filter(
                        student__id=student_id
                    )

                    if membership_requests.exists():  # Flow 2: Data found in GroupMembershipRequest
                        results = []
                        for request_item in membership_requests:
                            student = request_item.student
                            group = request_item.group

                            group_participant = GroupParticipant.objects.filter(
                                group_id=group).first()

                            idea_submissions = IdeaSubmission.objects.filter(
                                group_id=group
                            )

                            result_entry = {
                                "student_info": {
                                    "id": student.id,
                                    "full_name": student.full_name,
                                    "email": student.email,
                                    "institution": student.institution,
                                },
                                "group_info": {
                                    "name_of_group": group_participant.name_of_group if group_participant else None,
                                    "number_of_members": group_participant.number_of_member if group_participant else None,
                                    "project_type": group_participant.project_type if group_participant else None,
                                    "created_at": group_participant.created_at if group_participant else None,
                                },
                                "idea_submissions": [
                                    {
                                        "id": idea.id,
                                        "title": idea.title,
                                        "description": idea.description,
                                        "status": idea.status,
                                        "idea_file": idea.idea.url if idea.idea else None,
                                        "ppt_file": idea.ppt.url if idea.ppt else None,
                                        "video_file": idea.video_file.url if idea.video_file else None,
                                        "created_at": idea.created_at,
                                    }
                                    for idea in idea_submissions
                                ]
                            }

                            results.append(result_entry)

                        # If there is data in Flow 2, return the response
                        if results:
                            return Response({"data": results, "flow": "flow_2"}, status=status.HTTP_200_OK)
                        else:
                            # If Flow 2 returns no data, try Flow 3
                            flow = 'flow_3'
                    else:
                        # If Flow 2 does not return any data, move to Flow 3
                        flow = 'flow_3'

                elif flow == 'flow_3':
                    # --- FLOW 3: If no data from Flow 2, check for group created by the student ---
                    group_created_by_student = Group.objects.filter(
                        created_by=student_id).first()

                    if group_created_by_student:  # Flow 3: Group created by the student found
                        student = Student.objects.get(id=student_id)
                        group_participant = GroupParticipant.objects.filter(
                            group_id=group_created_by_student).first()
                        idea_submissions = IdeaSubmission.objects.filter(
                            group_id=group_created_by_student)

                        result_entry = {
                            "student_info": {
                                "id": student.id,
                                "full_name": student.full_name,
                                "email": student.email,
                                "institution": student.institution,
                            },
                            "group_info": {
                                "name_of_group": group_participant.name_of_group if group_participant else None,
                                "number_of_members": group_participant.number_of_member if group_participant else None,
                                "project_type": group_participant.project_type if group_participant else None,
                                "created_at": group_participant.created_at if group_participant else None,
                            },
                            "idea_submissions": [
                                {
                                    "id": idea.id,
                                    "title": idea.title,
                                    "description": idea.description,
                                    "status": idea.status,
                                    "idea_file": idea.idea.url if idea.idea else None,
                                    "ppt_file": idea.ppt.url if idea.ppt else None,
                                    "video_file": idea.video_file.url if idea.video_file else None,
                                    "created_at": idea.created_at,
                                }
                                for idea in idea_submissions
                            ]
                        }

                        return Response({"data": [result_entry], "flow": "flow_3"}, status=status.HTTP_200_OK)

                    return Response({"error": "No data found for the given student_id"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
