from django.db import models
from datetime import datetime


class Project(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Test(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(default=None)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    running_now = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Run(models.Model):
    run_at = models.DateTimeField(default=datetime.now, blank=True)


class RunTest(models.Model):
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    logs = models.TextField
    result = models.CharField(max_length=60)
