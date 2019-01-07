from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Project, Test
from .parse_project import update_projects, update_tests


def index(request):
    update_projects()
    projects = Project.objects.order_by('name')

    context = {
        'projects': projects
    }
    return render(request, 'web_gui/index.html', context)


def project(request, project_id):
    update_tests()
    project_name = get_object_or_404(Project, id=project_id)
    query = 'SELECT DISTINCT "web_gui_test"."id" ' \
            'FROM "web_gui_test" ' \
            'INNER JOIN "web_gui_project" on "web_gui_test"."project_id_id" = "web_gui_project"."id" where "web_gui_project"."id" = \'{}\''.format(str(project_id))
    tests = Test.objects.raw(query)

    context = {
        'project': project_name,
        'tests': tests,
    }
    return render(request, 'web_gui/project.html', context)

