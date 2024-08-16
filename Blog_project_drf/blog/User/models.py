from django.db import models

# Create your models here.

class UserSignup(models.Model):
    username=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=1000,blank=False,null=False)
    secretkey=models.CharField(max_length=100)
    email=models.EmailField(max_length=50,unique=True)
    contact=models.CharField(max_length=15)

class UserLogin(models.Model):
    user=models.ForeignKey(UserSignup,on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)
    login_session=models.DateTimeField(max_length=100)