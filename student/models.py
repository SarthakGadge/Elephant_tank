from django.db import models
from userauth.models import Student
# Create your models here.


class Group(models.Model):
    group_name = models.CharField(max_length=150, unique=True)
    created_by = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='created_groups')
    description = models.TextField(null=True, blank=True)
    is_open_for_joining = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name


class SingleParticipant(models.Model):
    stud_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    project_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    

class GroupParticipant(models.Model):
    stud_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    name_of_group = models.CharField(max_length=100)
    number_of_member = models.IntegerField()
    project_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)


class IdeaSubmission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('interested', 'Interested'),
        ('funded', 'Funded'),
        ('cancelled', 'Cancelled'),
    ]

    stud_id = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='submitted')
    idea = models.FileField(upload_to='idea/', null=False)
    ppt = models.FileField(upload_to='ppt/', null=True)
    project_type = models.CharField(max_length=50)
    name_of_group = models.CharField(max_length=100, null=True)
    number_of_member = models.IntegerField(null=True)
    video_file = models.FileField(upload_to='videos/', null=True)
    created_at = models.DateTimeField(auto_now=True)
    ai_score = models.CharField(max_length=50)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, blank=True)
    admin_approval = models.BooleanField(default=False)
    is_single_sub = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


class GroupMembershipRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='membership_requests')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='group_requests')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.group.group_name} ({self.status})"



