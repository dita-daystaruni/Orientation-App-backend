from django.db import models

class Activity(models.Model):
    '''Model for the activities'''
    title = models.CharField(max_length=200)
    description = models.TextField()
    time = models.TimeField()


    def __str__(self):
        '''String representation of the model'''
        return self.title
    
    class Meta:
       '''Meta class for the model'''
       pass
