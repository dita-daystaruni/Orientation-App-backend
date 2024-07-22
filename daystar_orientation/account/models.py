from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Account(AbstractUser):
    name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)


    groups = models.ManyToManyField(
        Group,
        related_name='account_users',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups'),
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='account_user_permissions',
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )
   

    REQUIRED_FIELDS = ['name', 'email', 'admission_number', 'course', 'phone_number']

    def __str__(self):
        return self.name