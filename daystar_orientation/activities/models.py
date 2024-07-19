from django.db import models

class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    time = models.TimeField()
   

    def __str__(self):
        return self.title
