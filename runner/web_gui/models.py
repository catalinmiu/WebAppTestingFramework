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
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    running_now = models.BooleanField(default=False)


class Run(models.Model):
    runned_at = models.DateTimeField(default=datetime.now, blank=True)


class Runed_test(models.Model):
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    logs = models.TextField
    result = models.CharField(max_length=60)



