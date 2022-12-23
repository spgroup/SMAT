from abc import ABC, abstractmethod

import os
import sys
import shutil
import subprocess
import threading

from collections import namedtuple
from nimrod.core.merge_scenario_under_analysis import MergeScenarioUnderAnalysis
from nimrod.project_info.merge_scenario import MergeScenario

from nimrod.utils import get_java_files
from nimrod.utils import generate_classpath
from nimrod.tools.bin import JUNIT, HAMCREST

TIMEOUT = 3000
COMPILE_TIMEOUT = 500

lock = threading.RLock()

Suite = namedtuple('Suite', ['suite_name', 'suite_dir', 'suite_classes_dir',
                             'test_classes'])


class SuiteGenerator(ABC):

    def __init__(self, java, classpath, tests_src, sut_class=None, sut_classes=None, sut_method=None, params=None, scenario: MergeScenario = None, input: MergeScenarioUnderAnalysis = None):
        self.java = java
        self.tests_src = tests_src
        self.classpath = classpath
        self.sut_class = sut_class
        self.sut_classes = sut_classes
        self.sut_method = sut_method
        self.parameters = params if params else []
        self.suite_dir = None
        self.suite_classes_dir = None
        self.suite_name = self._set_suite_name()
        self.scenario = scenario
        self.input = input

    @abstractmethod
    def _exec_tool(self):
        pass

    def _compile(self):
        self.suite_classes_dir = os.path.join(self.suite_dir, 'classes')
        self._create_dirs(self.suite_classes_dir)

        classpath = generate_classpath([self.classpath, self.suite_dir, JUNIT,
                                        HAMCREST, self.suite_classes_dir]
                                       + self._extra_classpath())

        for java_file in self._get_java_files():
            java_file = os.path.join(self.suite_dir, java_file)
            try:
                self.java.exec_javac(java_file, self._get_suite_dir(),
                                     self.java.get_env(), COMPILE_TIMEOUT,
                                     '-classpath', classpath,
                                     '-d', self.suite_classes_dir)
            except subprocess.CalledProcessError as e:
                print('[ERROR] Compiling {0} tests: {1}'.format(
                    self._get_tool_name(), e.output.decode('unicode_escape')),
                    file=sys.stderr)

    def _get_java_files(self):
        return sorted(get_java_files(self.suite_dir))

    @staticmethod
    def _extra_classpath():
        return []

    def _get_suite_dir(self):
        return self.suite_dir

    @abstractmethod
    def _test_classes(self):
        pass

    @staticmethod
    def _get_timeout():
        return TIMEOUT

    @staticmethod
    @abstractmethod
    def _get_tool_name():
        return "tool"

    def _exec(self, *command):
        try:
            return self.java.exec_java(self.suite_dir, self.java.get_env(),
                                       self._get_timeout(), *command)
        except subprocess.CalledProcessError as e:
            print('[ERROR] {0} call process error with command {1}: {2}'.format(
                self._get_tool_name(), command, e.output), file=sys.stderr)
            raise e
        except subprocess.TimeoutExpired:
            print('[WARNING] {0} timeout.')

    def _make_src_dir(self):
        self.suite_dir = os.path.join(self.tests_src, self.suite_name)
        self._create_dirs(self.suite_dir)

    def _set_suite_name(self):
        lock.acquire()
        self._create_dirs(self.tests_src, False)
        src_dirs = [file for file in os.listdir(self.tests_src)
                    if file.startswith(self._get_tool_name())]
        result = '{0}_{1}'.format(self._get_tool_name(), len(src_dirs) + 1)
        lock.release()
        return result

    @staticmethod
    def _create_dirs(path, remove_if_exists=True):
        if remove_if_exists and os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)

    def generate(self, make_dir=True):
        if make_dir:
            self._make_src_dir()
        self._exec_tool()
        self._compile()

        return Suite(suite_name=self.suite_name, suite_dir=self.suite_dir,
                     suite_classes_dir=self.suite_classes_dir,
                     test_classes=self._test_classes())
