
# Create your models here.
from django.db import models


# Create your views here.


class Employee(models.Model):
    username = models.CharField(max_length=20, primary_key=True, unique=True)
    first_name =  models.CharField(max_length=20)
    last_name = models.CharField(max_length=10)
    department = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, unique=True)

    def __str__(self):
        return self.username


class Employee2(models.Model):
    username = models.CharField(max_length=20, primary_key=True, unique=True)
    first_name =  models.CharField(max_length=20)
    last_name = models.CharField(max_length=10)
    department = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, unique=True)
    password  = models.CharField(max_length=40, default='1')

    def __str__(self):
        return self.username

