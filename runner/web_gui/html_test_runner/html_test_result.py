import threading
import time
from io import StringIO
from unittest import TestResult
import datetime

from web_gui.html_test_runner import save_images
from web_gui.html_test_runner.log.HandlerFactory import HandlerFactory
from web_gui.html_test_runner.log.Logger import GeneralLogger


class Result(TestResult):
    def __init__(self, verbosity=2):
        TestResult.__init__(self, verbosity=verbosity)
        super().__init__(verbosity=verbosity)
        self.success_count = 0
        self.failure_count = 0
        self.skip_count = 0
        self.error_count = 0
        self.success_set = set()
        self.failure_set = set()
        self.skip_set = set()
        self.error_set = set()
        self.stderr_steams = StringIO()
        self.stderr_steams.write("\n")
        self.stdout_steams = StringIO()
        self.stdout_steams.write("\n")
        """
        (
          result_code (0: success; 1: fail; 2: error; 3: skip),
          testCase_object,
          test_output (byte string),
          image_paths list,
        )
        """
        self.result = []
        self.result_tmp = {}
        self.time = {}

    def startTest(self, test):
        GeneralLogger().get_logger(True)
        GeneralLogger().get_logger().info("Start Test: {}".format(test))
        self.result_tmp[str(threading.current_thread().ident)] = {'result_code': 0,
                                                                  'testCase_object': test,
                                                                  'test_output': '',
                                                                  'image_paths': [],
                                                                  'startTime': str(datetime.datetime.now())[:19],
                                                                  'endTime': 0
                                                                  }
        self.time[str(threading.current_thread().ident)] = time.time()
        TestResult.startTest(self, test)

    def stopTest(self, test):
        end_time = time.time()
        GeneralLogger().get_logger().info("Stop Test: {}".format(test))
        GeneralLogger().get_logger().info("Duration: {}".format(
            end_time - self.time[str(threading.current_thread().ident)]))

        current_id = str(threading.current_thread().ident)
        if current_id in save_images.imageList:
            self.result_tmp[current_id]["image_paths"] = save_images.imageList.pop(current_id)
        self.result_tmp[current_id]['test_output'] = HandlerFactory.get_stream_value()
        self.result_tmp[current_id]['endTime'] = str(datetime.datetime.now())[:19]
        self.result.append(self.result_tmp.pop(current_id))

        if current_id in self.success_set:
            self.success_set.remove(current_id)
        if current_id in self.failure_set:
            self.failure_set.remove(current_id)
        if current_id in self.skip_set:
            self.skip_set.remove(current_id)
        if current_id in self.error_set:
            self.error_set.remove(current_id)

    def addSkip(self, test, reason):
        TestResult.addSkip(self, test, reason)
        self.stderr_steams.write('Skip\t')
        self.stderr_steams.write(str(test))
        doc = test._testMethodDoc
        if doc:
            self.stderr_steams.write("\t")
            self.stderr_steams.write(doc)
        self.stderr_steams.write("\n")

        GeneralLogger().get_logger().info(
            "Skip Test: {}\n{}".format(test, reason))

        current_id = str(threading.current_thread().ident)
        self.result_tmp[current_id]["result_code"] = 3
        if current_id not in self.skip_set:
            self.skip_count += 1
            self.skip_set.add(current_id)

    def addSuccess(self, test):
        TestResult.addSuccess(self, test)
        self.stdout_steams.write('Pass\t')
        self.stdout_steams.write(str(test))
        doc = test._testMethodDoc
        if doc:
            self.stdout_steams.write("\t")
            self.stdout_steams.write(doc)
        self.stdout_steams.write('\n')
        GeneralLogger().get_logger().info("Pass Test: {}".format(test))

        current_id = str(threading.current_thread().ident)
        self.result_tmp[current_id]["result_code"] = 0
        if current_id not in self.success_set:
            self.success_count += 1
            self.success_set.add(current_id)

    def addError(self, test, err):
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        self.stderr_steams.write('Error\t')
        self.stderr_steams.write(str(test))
        doc = test._testMethodDoc
        if doc:
            self.stderr_steams.write("\t")
            self.stderr_steams.write(doc)
        self.stderr_steams.write('\n')
        GeneralLogger().get_logger().error(
            "Error Test: {}\n{}".format(test, _exc_str))

        current_id = str(threading.current_thread().ident)
        self.result_tmp[current_id]["result_code"] = 2
        if current_id not in self.error_set:
            self.error_count += 1
            self.error_set.add(current_id)

    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        self.stderr_steams.write('Fail\t')
        self.stderr_steams.write(str(test))
        doc = test._testMethodDoc
        if doc:
            self.stderr_steams.write("\t")
            self.stderr_steams.write(doc)
        self.stderr_steams.write('\n')
        GeneralLogger().get_logger().warning(
            "Failure: {}\n{}".format(test, _exc_str))

        current_id = str(threading.current_thread().ident)
        self.result_tmp[current_id]["result_code"] = 1
        if current_id not in self.failure_set:
            self.failure_count += 1
            self.failure_set.add(current_id)
