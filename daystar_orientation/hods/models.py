from django.db import models

class HOD(models.Model):
    '''HODS model'''
    title = models.CharField(default='HOD', max_length=7)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    course = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        '''String representation of the model'''
        return self.first_name