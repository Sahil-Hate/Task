from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_picture = models.FileField(upload_to=None,blank=True, null=True)
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    
    def __str__(self):
            return self.username


class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_picture = models.FileField(upload_to=None,blank=True, null=True)
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username

    
class Blog(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="images",null=True,blank=True)
    category = models.CharField(max_length=255,null=True,blank=True)
    summary = models.CharField(max_length=255,null=True,blank=True)
    content = models.CharField(max_length=255,null=True,blank=True)
    publish_date = models.DateTimeField(auto_now_add=True, blank=True)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

CHOICES = (
    ("Yes", "yes"),
    ("No", "no"),
)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    speciality = models.CharField(max_length=255)
    appointment_date = models.DateField(null=True,blank=True)
    appointment_time = models.TimeField(auto_now=False, auto_now_add=False,unique=True) 

    def __str__(self):
        return str(self.patient) + " -- " + str(self.doctor)