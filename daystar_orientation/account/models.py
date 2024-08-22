from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models
import random
import string

class AccountManager(BaseUserManager):
    '''The user manager for the application'''

    def generate_password(self, admission_number):
        '''Password generation with four random letters and the admission number'''
        random_letters = ''.join(random.choices(string.ascii_uppercase, k=4))
        password = f"{random_letters}-{admission_number}"
        return password
    
    def create_user(self, email, username, first_name, last_name, admission_number, course, phone_number, user_type='regular', password=None, campus='Athi river', gender='Male', accomodation='Boarder'):
        '''Create a regular user'''
        if not admission_number:
            raise ValueError('Users must have an admission number')
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not password:
            raise ValueError('Users must have a password')
        if not phone_number:
            raise ValueError('Users must have a phone number')
        
        if password is None:
            password = self.generate_password(admission_number)

        if user_type not in Account.USER_TYPE_CHOICES_DICT:
            raise ValueError(f'Invalid user type: {user_type}. Must be one of {list(Account.USER_TYPE_CHOICES_DICT.keys())}.')
        if campus not in Account.CAMPUS_CHOICES_DICT:
            raise ValueError(f'Invalid campus: {campus}. Must be one of {list(Account.CAMPUS_CHOICES_DICT.keys())}.')
        if gender not in Account.GENDER_DICT:
            raise ValueError(f'Invalid gender: {gender}. Must be one of {list(Account.GENDER_DICT.keys())}.')
        if accomodation not in Account.ACCOMODATION_DICT:
            raise ValueError(f'Invalid accomodation type: {accomodation}. Must be one of {list(Account.ACCOMODATION_DICT.keys())}.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            campus=campus,
            admission_number=admission_number,
            course=course,
            gender=gender,
            accomodation=accomodation,
            phone_number=phone_number,
            user_type=user_type,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, admission_number, course, phone_number, password=None):
        '''Create a superuser for the application'''
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            admission_number=admission_number,
            course=course,
            phone_number=phone_number,
            user_type='admin',
            campus='Athi river',
            gender='Male',
            accomodation='Boarder',
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class Account(AbstractUser):
    '''The user model for the application '''
    USER_TYPE_CHOICES = (
        ('regular', 'Regular User (Freshman)'),
        ('parent', 'Parent (Orientation Lead)'),
        ('admin', 'Admin (G9)'),
    )

    CAMPUS_CHOICES = (
        ('Nairobi', 'Nairobi'),
        ('Athi river', 'Athi River'),
    )

    ACCOMODATION = (
        ('Boarder', 'Boarder'),
        ('Dayscholar', 'Dayscholar'),
    )

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    USER_TYPE_CHOICES_DICT = dict(USER_TYPE_CHOICES)
    CAMPUS_CHOICES_DICT = dict(CAMPUS_CHOICES)
    GENDER_DICT = dict(GENDER)
    ACCOMODATION_DICT = dict(ACCOMODATION)

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='regular')
    campus = models.CharField(max_length=12, choices=CAMPUS_CHOICES, default='Athi river')
    gender = models.CharField(max_length=8, choices=GENDER, default='Male')
    accomodation = models.CharField(max_length=12, choices=ACCOMODATION, default='Boarder')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    admission_number = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_first_time_user = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', limit_choices_to={'user_type': 'parent'})


    USERNAME_FIELD = 'admission_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'email', 'course', 'phone_number', 'password'] 

    objects = AccountManager()

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

    def __str__(self):
        return self.username