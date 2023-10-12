from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Profile (models.Model):
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    status=models.BooleanField(default=False)
    photo=models.ImageField(upload_to='profile_photos')
    user=models.OneToOneField(User, on_delete=models.CASCADE)



class Task(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=50)
    important=models.BooleanField(default=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

class Bitacora(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action=models.CharField(max_length=255)
    timestamp=models.DateField(default=timezone.now)