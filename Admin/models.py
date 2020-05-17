from django.db import models
from pytz import timezone
import  os
# Create your models here.
def path_photo(instance, filename):
    upload_to = 'media/members_photo/'
    ext = filename.split('.')[-1]
    filename = '{}_{}_{}.{}'.format(instance.member_id,instance.first_name,instance.last_name, ext)
    return os.path.join(upload_to, filename)
class MemberRegistration(models.Model):
    member_id = models.IntegerField()
    photo = models.ImageField(upload_to=path_photo)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class RegisterErrorLog(models.Model):
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    mobile = models.CharField(max_length=50,blank=True,null=True)
    error = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        datetime_obj_utc = self.created_at.astimezone(timezone('Asia/Kolkata')) 
        datetime_obj_utc = datetime_obj_utc.strftime("%Y-%m-%d-----%I:%M %p") 
        return (str(self.id) + ' -- ' +self.first_name + ' ' + self.last_name  + ' ' + self.mobile + ' ' + self.error + '--------------- ' + str(datetime_obj_utc))