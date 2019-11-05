from django.db import models
from  django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class Doggo(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.CharField(max_length=100)
    photo = models.ImageField(default=None)
    gender = models.IntegerField(default=None)

