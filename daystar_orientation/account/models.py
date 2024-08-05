from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models

class AccountManager(BaseUserManager):
    '''The user manager for the application'''
    
    def create_user(self, email, username, admission_number, course, phone_number, user_type='regular', password=None):
        '''Create a regular user'''
        if not admission_number:
            raise ValueError('Users must have an admission number')
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a user name')
        if not course:
            raise ValueError('Users must have a course')

        # Validate user_type against USER_TYPE_CHOICES
        if user_type not in Account.USER_TYPE_CHOICES_DICT:
            raise ValueError(f'Invalid user type: {user_type}. Must be one of {list(Account.USER_TYPE_CHOICES_DICT.keys())}.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            admission_number=admission_number,
            course=course,
            phone_number=phone_number,
            user_type=user_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, admission_number, course, phone_number, password=None):
        '''Create a superuser for the application'''
        user = self.create_user(
            email=email,
            username=username,
            admission_number=admission_number,
            course=course,
            phone_number=phone_number,
            user_type='admin',
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
    
    # User type choices as a dictionary
    USER_TYPE_CHOICES_DICT = dict(USER_TYPE_CHOICES)

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='regular')
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    admission_number = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'admission_number'
    REQUIRED_FIELDS = ['username', 'email', 'course', 'phone_number']

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