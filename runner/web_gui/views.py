from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Project


def index(request):
    projects = Project.objects.order_by('name')

    context = {
        'projects': projects
    }
    return render(request, 'web_gui/index.html', context)


def project(request, project_id):
    project_name = get_object_or_404(Project, id=project_id)
    context = {
        'project': project_name
    }
    return render(request, 'web_gui/project.html', context)

