import os
import fnmatch
from .models import Project, Test, Run, RunTest
from django.db import connection


def update_runned_tests(results):
    run = Run()
    run.save()
    for result in results:
        testCaseName = result['testCase_object'].__str__().split('projects.')[1].split('(')[0][:-1] + '.' + \
        result['testCase_object'].__str__().split('(')[0][:-1]
        project_name = testCaseName.split('.')[0]
        testCaseName = testCaseName.split('.')
        test_full_name = ""
        for i in testCaseName[1:]:
            test_full_name += i
            test_full_name += "."
        test_full_name = test_full_name[:-1]

        test = Test.objects.get(full_name=test_full_name,
                                project_id = Project.objects.get(name=project_name))

        runned_test = RunTest(run_id=run,
                              test_id=test,
                              logs=result['test_output'],
                              result=result['result_code'],
                              start_time=result['startTime'],
                              end_time=result['endTime']
                              )
        runned_test.save()
    return run.id
