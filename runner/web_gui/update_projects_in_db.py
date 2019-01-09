import os
import fnmatch
from .models import Project, Test
from django.db import connection


def get_all_projects():
    files_to_remove = ['__pycache__', '__init__.py', '.pytest_cache']
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
    projects_to_delete = set(projects_already_in_db) - set(projects_in_folder)
    for project in projects_to_delete:
        Project.objects.get(name=project).delete()
    projects_to_add = set(projects_in_folder)-set(projects_already_in_db)
    for i in projects_to_add:
        project = Project(name=i)
        project.save()


def update_tests():
    tests_to_project = get_tests_per_project()
    for project in list(tests_to_project.keys()):
        tests_already_in_db = [test.title for test in Test.objects.all().filter(project_id=Project.objects.get(name=project))]
        tests_in_folder = tests_to_project[project]

        # compare tests in project folder with tests in database
        tests_to_delete = set(tests_already_in_db) - set(tests_in_folder)
        for test in tests_to_delete:
            cursor = connection.cursor()
            query = """
            DELETE FROM "web_gui_test" 
            WHERE "web_gui_test"."id" IN
            (SELECT DISTINCT "web_gui_test"."id"
            FROM "web_gui_test"
            INNER JOIN "web_gui_project" on "web_gui_test"."project_id_id" = "web_gui_project"."id"
            WHERE "web_gui_project"."name" = {} and "web_gui_test"."title" = {})"""\
                .format(str(Project.objects.get(name=project)), test)
            cursor.execute(query)
            connection.commit()
        tests_to_add = set(tests_in_folder)-set(tests_already_in_db)
        for i in tests_to_add:
            test = Test(title=i, description='description', project_id=Project.objects.get(name=project))
            test.save()
