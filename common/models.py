"""
Common models for the DanWand scanner live site
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
#from PIL import Image
from django.contrib.auth.models import User  # pylint: disable=imported-auth-user

class Clinic(models.Model):
    """
    Store information of the individual Clinic
    """
    No = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], unique=True)
    Name = models.CharField(max_length=25)
    Logo = models.ImageField(blank=True)

class User2clinic(models.Model):
    """
    Maps users to the actual clinic
    From :model:`auth.User` to :model:`common.Clinic`.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

class Scanner(models.Model):
    """
    Contains information about the individual scanner
    """
    Serial = models.CharField(max_length=16, unique=True ) # used as deviceid
    Clinic = models.ForeignKey(Clinic, null=True, blank=True, on_delete=models.SET_NULL)
    LastRegister = models.DateTimeField(null=True, blank=True)
    Charge = models.IntegerField(null=True, blank=True)
    Name = models.CharField(max_length=20, blank=True)
    LocalIp = models.GenericIPAddressField(blank=True, null=True)
    RemoteIp = models.GenericIPAddressField(blank=True, null=True)
    HWmodel = models.CharField(max_length=40,null=True, blank=True)
    SWversion = models.CharField(max_length=20, null=True, blank=True)
    State = models.CharField(max_length=20, null=True, blank=True)
    CommandMode = models.CharField(max_length=20, null=True, blank=True)

# class Patient(models.Model):
#     PatientNo = models.IntegerField()
#     ClinicNo = models.ForeignKey(Clinic, on_delete=models.CASCADE)
#     Name = models.CharField(max_length= 50)

# class Picture(models.Model):
#     ClinicNo: models.ForeignKey(Clinic, on_delete=models.CASCADE)
#     Patient: models.ForeignKey(Patient, on_delete=models.CASCADE)
#     Scan: models.IntegerField()
#     Date: models.DateTimeField()
#     FilePath: models.CharField(max_length=25)
