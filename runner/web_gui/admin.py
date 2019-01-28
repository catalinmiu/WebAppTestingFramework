from django.contrib import admin

from .models import Project, Test, RunTest, Run

admin.site.register(Project)
admin.site.register(Test)
admin.site.register(Run)
admin.site.register(RunTest)
