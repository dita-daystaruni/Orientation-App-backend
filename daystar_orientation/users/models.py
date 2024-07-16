from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    admission_number = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email', 'admission_number', 'course', 'phone_number']
