from django.db import models
from django.utils.text import slugify
from User.models import UserSignup
from datetime import datetime


# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=20)

class Blogs(models.Model):
    title=models.CharField(max_length=100,unique=True)
    description=models.CharField(max_length=1000)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    slug=models.SlugField(max_length=200, unique=True, blank=True)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(UserSignup,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)