from django.shortcuts import render
from .models import Project


def index(request):
    project_list = Project.objects.order_by('name')

    context = {'project_list': project_list}
    return render(request, 'web_gui/index.html', context)
