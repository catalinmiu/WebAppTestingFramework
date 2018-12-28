from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Project


def index(request):
    project_list = Project.objects.order_by('name')

    context = {'project_list': project_list}
    return render(request, 'web_gui/index.html', context)


def project(request, project_id):
    project =get_object_or_404(Project, id=project_id)
    context = {'project': project}
    return render(request, 'web_gui/project.html', context)
