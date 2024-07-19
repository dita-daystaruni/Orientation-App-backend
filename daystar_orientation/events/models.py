from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='activity_photos/', null=True, blank=True)
    video = models.FileField(upload_to='activity_videos/', null=True, blank=True)

    def __str__(self):
        return self.title
