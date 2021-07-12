import os
import re
import time
import subprocess

from collections import namedtuple

from nimrod.tools.bin import JUNIT, HAMCREST, JMOCKIT, EVOSUITE_RUNTIME
from nimrod.utils import generate_classpath, package_to_dir
from nimrod.mutant import Mutant

TIMEOUT = 3000


JUnitResult = namedtuple('JUnitResult', ['ok_tests', 'ok_tests_number', 'fail_tests',
                                         'fail_test_set', 'fail_test_set_with_files', 'not_executed_test_set',
                                         'not_executed_test_set_with_files', 'flaky_test_set', 'run_time',
                                         'coverage', 'timeout'])


def is_failed_caused_by_compilation_problem(test_case_name, failed_test_message):
    my_regex = re.escape(test_case_name) + r"[0-9A-Za-z0-9_\(\.\)\n]+(NoSuchMethodError|NoSuchFieldError|NoSuchClassError|NoSuchAttributeError):"
    matches = re.findall(my_regex, failed_test_message)
    if (len(matches) > 0):
        return True
    else:
        return False

class JUnit:

    def __init__(self, java, classpath):
        self.java = java
        self.classpath = classpath
        
    def exec(self, suite_dir, suite_classes_dir, sut_class, test_class,
             timeout=TIMEOUT):
        classpath = generate_classpath([
            JMOCKIT, JUNIT, HAMCREST, EVOSUITE_RUNTIME,
            suite_classes_dir,
            self.classpath
        ])

        return self._exec(suite_dir, sut_class, test_class, classpath, '.',
                          timeout)

    def exec_with_mutant(self, suite_dir, suite_classes_dir, sut_class,
                         test_class, mutant_dir, timeout=TIMEOUT):
        classpath = generate_classpath([
            JMOCKIT, JUNIT, HAMCREST, EVOSUITE_RUNTIME,
            suite_classes_dir,
            mutant_dir,
            self.classpath
        ])

        return self._exec(suite_dir, sut_class, test_class, classpath,
                          mutant_dir, timeout)

    def _exec(self, suite_dir, sut_class, test_class, classpath,
              cov_src_dirs='.', timeout=TIMEOUT):

        params = (
            '-classpath', classpath,
            '-Dcoverage-classes=' + sut_class,
            '-Dcoverage-output=html',
            '-Dcoverage-metrics=line',
            '-Dcoverage-srcDirs=' + cov_src_dirs,
            'org.junit.runner.JUnitCore', test_class
        )

        start = time.time()
        try:
            output = self.java.exec_java(suite_dir, self.java.get_env(),
                                         timeout, *params)
            return JUnitResult(
                *JUnit._extract_results_ok(output.decode('unicode_escape')),
                time.time() - start, None, False
            )
        except subprocess.CalledProcessError as e:
            print(e)
            return JUnitResult(
                *JUnit._extract_results(e.output.decode('unicode_escape')),
                time.time() - start, None, False
            )
        except subprocess.TimeoutExpired as e:
            print(e)
            elapsed_time = time.time() - start
            print("# [WARNING] Run JUnit tests timed out. {0} seconds".format(
                elapsed_time))
            return JUnitResult(set, 0, 0, set(), set(), set(), set(), set(), 0, None, True)

    @staticmethod
    def _extract_results_ok(output):
        result = re.findall(r'OK \([0-9]* tests?\)', output)
        if len(result) > 0:
            result = result[0].replace('(', '')
            r = [int(s) for s in result.split() if s.isdigit()]
            return set(), r[0], 0, set(), set(), set(), set(), set()

        return set, 0, 0, set(), set(), set(), set(), set()

    @staticmethod
    #trabalhar para extrair o conjunto de testes que passaram.
    def _extract_results(output):
        if len(re.findall(r'initializationError', output)) == 0:
            result = re.findall(r'Tests run: [0-9]*,[ ]{2}Failures: [0-9]*',
                                output)
            if len(result) > 0:
                result = result[0].replace(',', ' ')
                r = [int(s) for s in result.split() if s.isdigit()]
                result = JUnit._extract_test_id(output)
                return result[2], len(result[2]), r[1], result[0], result[3], result[1], result[4], set()

        return set(), 0, 0, set(), set(), set(), set(), set()

    @staticmethod
    def _extract_test_id(output):
        tests_fail = set()
        tests_not_executed = set()
        tests_fail_with_files = set()
        tests_not_executed_with_files = set()
        list_failed_tests = []

        list_failed_tests = re.findall(r'test[0-9]+\([A-Za-z0-9_.]+\)', output)
        number_executed_tests = int(re.findall('Tests run: \d+', output)[0].split("Tests run: ")[-1])
        for test in list_failed_tests:
            i = re.findall('\d+', test)
            test_case = re.findall(r'.+?(?=\()', test)[0]
            file = str(re.findall(r'\(.+?(?=\))', test)[0]).split(".")[-1] #re.findall(r'\(.+?(?=\))', test)[0][1:].to_s.split(".")[-1]

            if len(i) > 0:
                if ((is_failed_caused_by_compilation_problem(test_case, output) == True)):
                    print("\n*** ERROR: test case "+test_case+" was not executable in project version. \n")
                    tests_not_executed_with_files.add('{0}#{1}'.format(file, test_case, int(i[-1])))
                    tests_not_executed.add(test_case)
                else:
                    print("\n*** Failed: test case " + test_case + ". \n")
                    tests_fail_with_files.add('{0}#{1}'.format(file, test_case, int(i[-1])))
                    tests_fail.add(test_case)
            else:
                print("*** ERROR: Error in regex of junit output.")
        executed_tests = set()
        for i in range(0, number_executed_tests):
            if not ('test'+str(i) in tests_fail) and not ('test'+str(i) in tests_not_executed):
                value = 'test'+str(i)
                executed_tests.add(value)

        return tests_fail, tests_not_executed, executed_tests, tests_fail_with_files, tests_not_executed_with_files

    def run_with_mutant(self, suite, sut_class, mutant_dir, cov_original=True,
                        original_dir=None):
        executions_test = []
        ok_tests = set()
        ok_tests_number = 0
        fail_tests = 0
        fail_test_set = set()
        fail_test_set_with_files = set()
        not_executed_test_set = set()
        not_executed_test_set_with_files = set()
        run_time = 0
        call_points = set()
        test_cases = set()
        class_coverage = dict()
        executions = 0
        timeout = False
        flaky_test_set = set()

        for i in range(0, 1):
            for test_class in suite.test_classes:
                result = self.exec_with_mutant(suite.suite_dir,
                                               suite.suite_classes_dir, sut_class,
                                               test_class, mutant_dir)
                ok_tests = result.ok_tests
                ok_tests_number = result.ok_tests_number
                fail_tests += result.fail_tests
                not_executed_test_set = result.not_executed_test_set
                not_executed_test_set_with_files = result.not_executed_test_set_with_files
                fail_test_set = result.fail_test_set
                fail_test_set_with_files = result.fail_test_set_with_files
                run_time += run_time
                timeout = timeout or result.timeout
                flaky_test_set = result.flaky_test_set

                if not timeout:
                    if cov_original:
                        if original_dir is None:
                            original_dir = os.path.join(
                                mutant_dir[:mutant_dir.rfind(os.sep)], 'ORIGINAL')
                        if os.path.exists(original_dir):
                            self.java.compile_all(self.classpath, original_dir)
                            result_original = self.exec_with_mutant(suite.suite_dir,
                                                  suite.suite_classes_dir,
                                                  sut_class, test_class,
                                                  self.get_original(original_dir))
                            if result_original.fail_tests > 0:
                                #Se os testes tb falham no original e são os mesmos teste que falahm no mutante.
                                #Logo devem ser Equivalentes.
                                if result_original.fail_test_set == result.fail_test_set:
                                    fail_tests = 0
                                    fail_test_set = set()
                        else:
                            print('[WARNING] ORIGINAL class not found in {0}, using'
                                  ' mutant in coverage.'.format(original_dir))
                else:
                    r = self.exec(suite.suite_dir, suite.suite_classes_dir,
                                  sut_class, test_class)
                    if r.timeout:
                        return None

            executions_test.append(JUnitResult(ok_tests, ok_tests_number, fail_tests, fail_test_set, fail_test_set_with_files, not_executed_test_set,not_executed_test_set_with_files, flaky_test_set, run_time,Coverage(call_points, test_cases, executions,class_coverage),timeout))

        return self.check_for_consistent_test_results(executions_test)

    def check_for_consistent_test_results(self, executions):
        failed_test_set = set()
        stable_execution = None
        stable_failed_test_cases = set()
        for one_execution in executions:
            if (stable_execution == None):
                stable_execution = one_execution
                stable_failed_test_cases = one_execution.fail_test_set
            stable_failed_test_cases = stable_failed_test_cases.intersection(one_execution.fail_test_set)
            failed_test_set = failed_test_set.union(one_execution.fail_test_set)
        final_failed_test_set = failed_test_set.difference(stable_failed_test_cases)

        if (final_failed_test_set == set()):
            return stable_execution
        else:
            stable_execution.fail_test_set = self.discard_unstable_failed_tests(final_failed_test_set, stable_execution.fail_test_set)
            stable_execution.not_executed_test_set = self.discard_unstable_failed_tests(final_failed_test_set, stable_execution.not_executed_test_set)
            stable_execution.fail_test_set_with_files = self.discard_unstable_failed_tests(final_failed_test_set, stable_execution.fail_test_set_with_files)
            stable_execution.not_executed_test_set_with_files = self.discard_unstable_failed_tests(final_failed_test_set, stable_execution.not_executed_test_set_with_files)
            stable_execution.ok_tests = self.discard_unstable_failed_tests(final_failed_test_set, stable_execution.ok_tests)
            stable_execution.flaky_test_set = final_failed_test_set
            return stable_execution

    def discard_unstable_failed_tests(self, unstable_failed_tests, test_cases_set):
        test_cases_to_remove = set()
        for unstable_failed_test in unstable_failed_tests:
            for test_cases_set_one in test_cases_set:
                if (str(unstable_failed_test) in str(test_cases_set_one)):
                    test_cases_to_remove.add(test_cases_set_one)

        for test_case_one in test_cases_to_remove:
            test_cases_set.remove(test_case_one)

        return test_cases_set

    @staticmethod
    def get_original(original_dir):
        return Mutant(mid='ORIGINAL', operator=None, line_number=None,
                      method=None, transformation=None, dir=original_dir)

    @staticmethod
    def run_coverage(suite_dir, sut_class, mutation_line):
        jmockit = JMockit(suite_dir, sut_class)
        return jmockit.coverage(mutation_line)


Coverage = namedtuple('Coverage', ['call_points', 'test_cases', 'executions', 'class_coverage'])


class JMockit:

    def __init__(self, suite_dir, sut_class):
        self.suite_dir = suite_dir
        self.sut_class = sut_class

    def coverage(self, mutation_line):
        return self.get_coverage_report(mutation_line)

    def get_coverage_report(self, mutation_line):
        report_file = self.get_coverage_report_file()

        #if report_file:
            #with open(report_file, 'r') as html:
                #soup = BeautifulSoup(html, 'html.parser')
                #return JMockit._get_coverage_info(soup, mutation_line)

    def get_coverage_report_file(self):
        coverage_report = os.path.join(self.suite_dir, 'coverage-report',
                                       package_to_dir(self.sut_class) + '.html')

        return coverage_report if os.path.exists(coverage_report) else None

    @staticmethod
    def _get_coverage_info(soup, mutation_line):
        test_cases = set()
        call_points = set()
        executions = 0

        for tr in soup.find_all('tr'):
            td_line = tr.find_all('td', class_='line')
            td_executions = tr.find_all('td', class_='count')
            td_count = tr.find_all('td', class_='callpoints-count')
            if (td_line and td_count and td_executions
                    and mutation_line == int(td_line[0].string)):
                executions = int(td_executions[0].string.strip())
                for li in tr.find_all('li'):
                    info = JMockit._extract_li(li)
                    if info:
                        file, test_case, cps = info
                        test_cases.add((file, test_case))
                        for cp in cps:
                            call_points.add((file, test_case, cp))

        class_coverage =  JMockit._get_coverage_info_class(soup)
        return Coverage(call_points, test_cases, executions, class_coverage)



    @staticmethod
    def _get_coverage_info_class(soup):
        executions = 0
        class_coverage_line = dict()

        for tr in soup.find_all('tr'):
            td_line = tr.find_all('td', class_='line')
            td_executions = tr.find_all('td', class_='count')
            td_count = tr.find_all('td', class_='callpoints-count')
            if (td_line and td_count and td_executions):
                line = int(td_line[0].string)
                executions = int(td_executions[0].string.strip())
                class_coverage_line[line] = executions
        return class_coverage_line

    @staticmethod
    def _extract_li(li):
        li = li.string.split(':')
        if len(li) == 2:
            try:
                file = li[0].split('#')[0]
                test_case = li[0].split('#')[1]
                return (file, test_case,
                        [int(cp.split('x')[0].strip())
                         for cp in li[1].split(',')])
            except IndexError:
                return None