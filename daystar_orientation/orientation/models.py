from django.db import models

class Orientation(models.Model):
    '''Orientation model'''
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    venue = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='event_photos/', null=True, blank=True)
    video = models.FileField(upload_to='event_videos/', null=True, blank=True)

    def __str__(self):
        return self.description
    
    class Meta:
        '''Meta class for the model'''
        pass
