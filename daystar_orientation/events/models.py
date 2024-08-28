from django.db import models

class Event(models.Model):
    '''Model for the events'''
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        '''Meta class for the model'''
        pass
