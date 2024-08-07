from django.db import models

class Notification(models.Model):
    '''Model for the notifications'''
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        '''String representation of the model'''
        return self.title
    
    class Meta:
       '''Meta class for the model'''
       pass
