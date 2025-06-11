from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    summary = models.TextField()
    date_posted = models.CharField(max_length=100)

    def __str__(self):
        return self.title