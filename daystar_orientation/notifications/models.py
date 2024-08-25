from django.conf import settings
from django.db import models
from account.models import Account  # Import the Account model

class Notification(models.Model):
    '''Model for the notifications'''
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        related_name='notifications',
        null=True
    )
    viewers = models.ManyToManyField('account.Account', related_name='viewable_notifications', blank=True, limit_choices_to={'user_type__in': ['admin', 'parent', 'regular']})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''String representation of the model'''
        return self.title

    class Meta:
        '''Meta class for the model'''
        ordering = ['-created_at']
