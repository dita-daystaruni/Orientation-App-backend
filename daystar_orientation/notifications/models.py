from django.conf import settings
from django.db import models

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
    is_admin_viewer = models.BooleanField(default=False)
    is_parent_viewer = models.BooleanField(default=False)
    is_regular_viewer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''String representation of the model'''
        return self.title

    class Meta:
        '''Meta class for the model'''
        ordering = ['-created_at']
