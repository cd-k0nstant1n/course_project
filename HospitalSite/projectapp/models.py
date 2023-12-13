from django.db import models

# Create your models here.
class Patient(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=13)
    password = models.CharField(max_length=1000)
    
class Doctor(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=13)
    specialty = models.EmailField(max_length=100)
    password = models.CharField(max_length=1000)
    
class Code(models.Model):
    code = models.CharField(max_length=1000)