from django.db import models

class FAQ(models.Model):
    '''Model for the faqs'''
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question

    class Meta:
      pass