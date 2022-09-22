import logging
import re
import subprocess
from os import path
from typing import Dict, List
from nimrod.test_suite_generation.test_suite import TestSuite
from nimrod.test_suites_execution.test_case_result import TestCaseResult
from nimrod.tests.utils import get_base_output_path
from nimrod.tools.bin import EVOSUITE_RUNTIME, JUNIT
from nimrod.tools.java import TIMEOUT, Java
from nimrod.tools.jacoco import Jacoco
from nimrod.utils import generate_classpath

def is_failed_caused_by_compilation_problem(test_case_name: str, failed_test_message: str) -> bool:
    my_regex = re.escape(test_case_name) + r"[0-9A-Za-z0-9_\(\.\)\n \:]+(NoSuchMethodError|NoSuchFieldError|NoSuchClassError|NoClassDefFoundError|NoSuchAttributeError|tried to access method)"
    return re.search(my_regex, failed_test_message) != None

def is_failed_caused_by_error(test_case_name: str, failed_test_message: str) -> bool:
    my_regex = re.escape(test_case_name) + r"[0-9A-Za-z0-9_(.)]RegressionTest[0-9A-Za-z0-9_(.)\n]+Exception"
    return re.search(my_regex, failed_test_message) != None

def get_result_for_test_case(failed_test: str, output: str) -> TestCaseResult:
    if is_failed_caused_by_compilation_problem(failed_test, output):
        return TestCaseResult.NOT_EXECUTABLE
    elif is_failed_caused_by_error(failed_test, output):
        return TestCaseResult.FAIL
    return TestCaseResult.FAIL

class TestSuiteExecutor:
    def __init__(self, java: Java, jacoco: Jacoco) -> None:
        self._java = java
        self._jacoco = jacoco

    def execute_test_suite(self, test_suite: TestSuite, jar: str, number_of_executions: int = 3) -> Dict[str, TestCaseResult]:
        results: Dict[str, TestCaseResult] = dict()

        for test_class in test_suite.test_classes_names:
            for i in range(0, number_of_executions):
                logging.debug("Starting execution %d of %s from suite %s", i + 1, test_class, test_suite.path)
                response = self._execute_junit(test_suite, jar, test_class)
                for test_case, test_case_result in response.items():
                    if results.get(test_case) and results.get(test_case) != test_case_result:
                        results[test_case] = TestCaseResult.FLAKY
                    elif not results.get(test_case):
                        results[test_case] = test_case_result

        return results

    def _execute_junit(self, test_suite: TestSuite, target_jar: str, test_class: str, extra_params: List[str] = []) -> Dict[str, TestCaseResult]:
        try:
            classpath = generate_classpath([
                JUNIT,
                EVOSUITE_RUNTIME,
                target_jar,
                test_suite.class_path
            ])

            params = [
                '-classpath', classpath,
                'org.junit.runner.JUnitCore', test_class
            ] + extra_params

            command = self._java.exec_java(test_suite.path, self._java.get_env(), TIMEOUT, *params)
            output = command.decode('unicode_escape')

            return self._parse_test_results_from_output(output)
        except subprocess.CalledProcessError as error:
            output = error.output.decode('unicode_escape')
            return self._parse_test_results_from_output(output)

    def _parse_test_results_from_output(self, output: str) -> Dict[str, TestCaseResult]:
        results: Dict[str, TestCaseResult] = dict()

        success_match = re.search(r'OK \((?P<number_of_tests>\d+) tests?\)', output)
        if success_match:
            number_of_tests = int(success_match.group('number_of_tests'))
            for i in range(0, number_of_tests):
                test_case_name = 'test{number:0{width}d}'.format(width=len(str(number_of_tests)), number=i)
                results[test_case_name] = TestCaseResult.PASS
        else:
            failed_tests = re.findall(r'(?P<test_case_name>test\d+)\([A-Za-z0-9_.]+\)', output)
            for failed_test in failed_tests:
                results[failed_test] = get_result_for_test_case(failed_test, output)

            tests_run = re.search(r'Tests run: (?P<tests_run_count>\d+),', output)
            test_run_count = 0
            if tests_run:
                test_run_count = int(tests_run.group('tests_run_count'))
            for i in range(0, test_run_count):
                test_case_name = 'test{number:0{width}d}'.format(width=len(str(test_run_count)), number=i)
                if not results.get(test_case_name):
                    results[test_case_name] = TestCaseResult.PASS
 
        return results

    def execute_test_suite_with_coverage(self, test_suite: TestSuite, target_jar: str, test_cases: List[str], watched_classes: List[str]) -> str:
        instrumented_jars_path = path.join(
            get_base_output_path(), "instrumented_jars")

        logging.debug(f'Starting instrumentation of jar {target_jar}')
        self._jacoco.execInstrumentJar(target_jar, instrumented_jars_path)
        logging.debug(f'Successfully instrumented jar {target_jar}')

        return path.join(instrumented_jars_path, target_jar.split('/')[-1])
