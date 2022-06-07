from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    first_name = models.CharField(max_length=255,unique=True)
    last_name = models.CharField(max_length=255,unique=True)
    profile_picture = models.FileField(upload_to=None,blank=True, null=True)
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255,unique=True)
    address = models.CharField(max_length=255,unique=True)
    
    def __str__(self):
            return self.username


class Patient(models.Model):
    first_name = models.CharField(max_length=255,unique=True)
    last_name = models.CharField(max_length=255,unique=True)
    profile_picture = models.FileField(upload_to=None,blank=True, null=True)
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255,unique=True)
    address = models.CharField(max_length=255,unique=True)
    
    def __str__(self):
            return self.username

    