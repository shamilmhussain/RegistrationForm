from django.db import models

# Create your models here.

class MemberRegistration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    dob = models.DateField()
    blood_group = models.CharField(max_length=10)
    unit = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    central = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    islamic = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    skills = models.TextField()
    district = models.CharField(max_length=25)
    house_name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    post_office = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)