from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator
# Create your models here.


class Student(models.Model):
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=50, validators=[EmailValidator()])
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=10)
    role = models.CharField(max_length=50, default='Student')
    linked_url = models.CharField(max_length=150)
    institution = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    max_otp_try = models.IntegerField(default=3)
    otp_max_out = models.DateTimeField(null=True, blank=True)
    password_reset_otp = models.CharField(max_length=6, null=True, blank=True)
    password_reset_otp_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_group = models.BooleanField(default=False)
    address = models.TextField()
    postal_code = models.CharField(max_length=50)
    country = models.CharField(max_length=200)
    date_of_birth = models.CharField(max_length=50, null=True, blank=True)
    city =  models.CharField(max_length=200)
    state =  models.CharField(max_length=200)
    is_group_leader = models.BooleanField(default=False)
    admin_approval = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M', 
    )
    field_of_study = models.CharField(max_length=50)
    graduation_year = models.IntegerField()
    graduation_degree = models.CharField(max_length=150, null=True, blank=True )
    is_group = models.BooleanField(default=False)
    group_name = models.CharField(max_length=150, null=True, blank=True)
    group_members = models.CharField(null=True, blank=True , max_length=350)
    post_graduation_degree = models.CharField(max_length=150, null=True, blank=True)

    def is_otp_valid(self):
        if self.otp and self.otp_expiry:
            return timezone.now() <= self.otp_expiry
        return False

    def can_send_otp(self):
        if self.otp_max_out:
            return timezone.now() > self.otp_max_out
        return self.max_otp_try > 0


class Investor(models.Model):
    full_name = models.CharField(max_length=250)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=10)
    role = models.CharField(max_length=50, default='Investor')
    domain = models.CharField(max_length=150)
    linked_url = models.CharField(max_length=150)
    gender = models.CharField(max_length=50)
    organisation = models.CharField(max_length=150)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    max_otp_try = models.IntegerField(default=3)
    otp_max_out = models.DateTimeField(null=True, blank=True)
    password_reset_otp = models.CharField(max_length=6, null=True, blank=True)
    password_reset_otp_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    admin_approval = models.BooleanField(default=False)

    def is_otp_valid(self):
        if self.otp and self.otp_expiry:
            return timezone.now() <= self.otp_expiry
        return False

    def can_send_otp(self):
        if self.otp_max_out:
            return timezone.now() > self.otp_max_out
        return self.max_otp_try > 0
