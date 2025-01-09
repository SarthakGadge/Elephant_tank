from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    joining_date = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=10)
    emergency_contact = models.CharField(max_length=15)
    dob = models.DateField()
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=150)

    class Meta:
        db_table = 'admin'
