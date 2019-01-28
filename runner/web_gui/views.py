from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Project, Test, Run, RunTest
from .update_projects_in_db import update_projects, update_tests
from .put_set_tests_to_db import update_runned_tests
from django.shortcuts import redirect

import importlib
import argparse
import unittest
import os
import sys
import time
from .html_test_runner.html_test_runner import TestRunner

def index(request):
    update_projects()
    projects = Project.objects.order_by('name')

    context = {
        'projects': projects
    }
    return render(request, 'web_gui/index.html', context)

def runnedTests(request):
    query = 'SELECT DISTINCT * ' \
            'FROM "web_gui_run" '

    tests = Run.objects.raw(query)
    context = {
        'tests': tests
    }
    return render(request, 'web_gui/runnedTests.html', context)

def runnedTest(request, runnedtest_id):
    query = 'SELECT DISTINCT * ' \
            'FROM "web_gui_run" ' \
            'INNER JOIN "web_gui_runtest" on "web_gui_runtest"."run_id_id" = "web_gui_run"."id" ' \
            'INNER JOIN "web_gui_test" on "web_gui_runtest"."test_id_id" = "web_gui_test"."id"' \
            'where "web_gui_runtest"."id" = \'{}\''.format(str(runnedtest_id))
    test = RunTest.objects.raw(query)[0]
    context = {
        'test': test,
    }
    return render(request, 'web_gui/runnedtest.html', context)


def raport(request, raport_id):
    query = 'SELECT DISTINCT * ' \
            'FROM "web_gui_run" ' \
            'INNER JOIN "web_gui_runtest" on "web_gui_runtest"."run_id_id" = "web_gui_run"."id" ' \
            'INNER JOIN "web_gui_test" on "web_gui_runtest"."test_id_id" = "web_gui_test"."id"'\
            'WHERE "web_gui_run"."id" = \'{}\''.format(str(raport_id))
    tests = Run.objects.raw(query)
    success = 0
    fail = 0
    error = 0
    skip = 0
    for i in tests:
        if i.result == 0:
            success += 1
        elif i.result == 1:
            fail += 1
        elif i.result == 2:
            error += 1
        elif i.result == 3:
            skip += 1
    context = {
        'tests': tests,
        'success': success,
        'fail': fail,
        'error': error,
        'skip': skip
    }
    return render(request, 'web_gui/raport.html', context)



def  _create_html_results_folder():
    cwd = os.getcwd()
    results_path = '{}/output/{}'.format(cwd, "asd")
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    return results_path


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
    if request.POST:
        checkList = request.POST.getlist('checks')
        tests = []
        for p in checkList:
            test_name = get_object_or_404(Test, id=p)
            tests.append(test_name)
        suite1 = []
        for p in tests:
            numeTest = p.__str__()
            fullName = p.full_name
            className = fullName.split(numeTest)[0].split('.')[-2]
            path = fullName.split(numeTest)[0].split(className)[0][:-1]
            # className2 = importlib.import_module('projects.ib.' + path)
            className = getattr(importlib.import_module('projects.' + project_name.__str__() + '.' + path), className)
            suite1.append(className(numeTest))
        big_suite = unittest.TestSuite()
        for test_class in suite1:
            big_suite.addTest(test_class)



        html_results_path = _create_html_results_folder()
        filename = '{timestamp}.html'.format(timestamp=time.strftime("%Y%m%d-%H%M%S"))
        test_result = TestRunner(
            title="asd",
            output_path='{}/{}'.format(html_results_path, filename),
        ).run(big_suite)

        runnedTestsPage = update_runned_tests(test_result.result)
        return redirect('/raport/' + str(runnedTestsPage))

    return render(request, 'web_gui/project.html', context)
