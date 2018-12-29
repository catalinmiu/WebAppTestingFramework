import os
import fnmatch
from runner.web_gui.models import Project, Test


def get_all_projects():
    files_to_remove = ['__pycache__', '__init__.py']
    files = os.listdir('./projects')
    for file in files_to_remove:
        try:
            files.remove(file)
        except ValueError:
            pass
    return files


def get_tests_per_project():
    tests_per_project = {}
    for project in get_all_projects():
        tests = [
            file for (root, dirs, files) in os.walk(f'./projects/{project}')
            for file in files if fnmatch.fnmatch(file, 'test_*.py')
        ]
        tests_per_project[project] = tests
    return tests_per_project


def update_projects():
    projects_already_in_db = [value.name for value in Project.objects.all()]
    projects_in_folder = get_all_projects()

    # compare projects in folder with projects in database
    projects_to_add = set(projects_in_folder)-set(projects_already_in_db)
    for i in projects_to_add:
        project = Project(name=i)
        project.save()
    projects_to_delete = set(projects_already_in_db)-set(projects_in_folder)
    for project in projects_to_delete:
        project.delete()


def update_tests():
    tests_to_project = get_tests_per_project()
    for project in list(tests_to_project.keys()):
        tests_already_in_db = [
            test.title for test in Test.objects.all().filter(project_id=Project.objects.get(name='selenium_project'))
        ]
        tests_in_folder = list(project.values())

        # compare tests in project folder with tests in database
        tests_to_add = set(tests_in_folder)-set(tests_already_in_db)
        for i in tests_to_add:
            test = Test(title=i, description='description', project_id=Project.objects.get(name=project))
            test.save()
        tests_to_delete = set(tests_already_in_db)-set(tests_in_folder)
        for test in tests_to_delete:
            test.delete()
