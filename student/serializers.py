from investor.models import InvestorInterest
from student.models import SingleParticipant, GroupParticipant, IdeaSubmission
from rest_framework import serializers
from userauth.models import Investor
from .models import GroupMembershipRequest
from .models import Group


class SingleParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleParticipant
        fields = '__all__'


class GroupParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupParticipant
        fields = '__all__'


class IdeaSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaSubmission
        fields = '__all__'


class GroupMembershipRequestSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    group = serializers.StringRelatedField()

    class Meta:
        model = GroupMembershipRequest
        fields = ['id', 'group', 'student',
                  'status', 'requested_at', 'updated_at']


class GroupSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'created_by',
                  'description', 'is_open_for_joining', 'created_at']


class InvestorSerializerForStudentInterest(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ["id", "full_name", "email", "phone_number", "domain", "linked_url", "gender", "organisation"]


class InvestorForStudentSerailizer(serializers.ModelSerializer):
    investor = InvestorSerializerForStudentInterest()  

    class Meta:
        model = InvestorInterest
        fields = ['id', 'investor', 'datetime','amount_range']
