from django.db import models
from datetime import datetime


class Project(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Test(models.Model):
    title = models.TextField(default=None)
    full_name = models.TextField(max_length=250, default=False)
    description = models.TextField(default=None)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    running_now = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Run(models.Model):
    run_at = models.DateTimeField(default=datetime.now, blank=True)


class RunTest(models.Model):
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE, null=True)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    logs = models.TextField(default=None)
    result = models.IntegerField(default=-1)
    start_time = models.TextField(default=None)
    end_time = models.TextField(default=None)

