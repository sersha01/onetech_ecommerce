from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    phone = models.IntegerField(null=True)
    status = models.BooleanField(default=True, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to='profile_pic', default='profile_pic/male-avatar.jpg')


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    address = models.TextField(null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pincode = models.IntegerField(null=True)
    number = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    