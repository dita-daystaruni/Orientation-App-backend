from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Account(AbstractUser):
    '''The user model for the application '''
    USER_TYPE_CHOICES = (
        ('regular', 'Regular User (Freshman)'),
        ('parent', 'Parent (Orientation Lead)'),
        ('admin', 'Admin (G9)'),)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='regular')
    name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    #parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')


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

    def save(self, *args, **kwargs):
        '''Save the user and assign permissions based on user type'''
        super().save(*args, **kwargs)
        if self.user_type == 'admin':
            self.user_permissions.set(Permission.objects.all())
        elif self.user_type == 'parent':
            view_permissions = Permission.objects.filter(codename__startswith='view_')
            self.user_permissions.set(view_permissions)
        elif self.user_type == 'regular':
            view_permissions = Permission.objects.filter(codename__startswith='view_')
            self.user_permissions.set(view_permissions)