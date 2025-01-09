from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


class Applicant(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    institution = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    graduation_year = models.PositiveIntegerField()
    gender = models.CharField(max_length=50)
    graduation_degree = models.CharField(max_length=255)
    post_graduation_degree = models.CharField(max_length=255)
    cover_letter = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    resume_upload = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt'])]
    )

    def __str__(self):
        return self.full_name

# Signal to send email on applicant creation
@receiver(post_save, sender=Applicant)
def send_congratulation_email(sender, instance, created, **kwargs):
    if created:  # Check if the instance is newly created
        subject = "Congratulations on Your Application Submission!"
        message = f"""
        Dear {instance.full_name},

        Thank you for submitting your application to our system. We have successfully received your details.
        
        Here are your application details:
        - Name: {instance.full_name}
        - Email: {instance.email}
        - Phone: {instance.phone_number}

        We will review your application and get back to you shortly.

        Best Regards,
        The Elephant Tank Team
        """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]  # Send email to the applicant's email address
        send_mail(subject, message, from_email, recipient_list)
