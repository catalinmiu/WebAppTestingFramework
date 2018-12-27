from django.db import models
from datetime import datetime


class Project(models.Model):
    PROJECTS = (
        ('Selenium Project', 'Selenium Project'),
        ('Dummy Project', 'Dummy Project'),
    )
    name = models.CharField(max_length=40, choices=PROJECTS)

    def __str__(self):
        return self.name


class Test(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField
    created_at = models.DateTimeField(default=datetime.now, blank=True)
