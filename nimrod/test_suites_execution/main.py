import logging
from typing import Dict, List
from nimrod.test_suite_generation.test_suite import TestSuite
from nimrod.input_parsing.smat_input import ScenarioInformation as ScenarioJars
from nimrod.test_suites_execution.test_case_result import TestCaseResult
from nimrod.test_suites_execution.test_case_execution_in_merge_scenario import TestCaseExecutionInMergeScenario
from nimrod.test_suites_execution.test_suite_executor import TestSuiteExecutor

class TestSuitesExecution:
    def __init__(self, test_suite_executor: TestSuiteExecutor) -> None:
        self._test_suite_executor = test_suite_executor

    def execute_test_suites(self, test_suites: List[TestSuite], scenario_jars: ScenarioJars) -> List[TestCaseExecutionInMergeScenario]:
        results: List[TestCaseExecutionInMergeScenario] = []

        for test_suite in test_suites:
            logging.info("Starting execution of %s test suite in base", test_suite.generator_name)
            results_base = self._test_suite_executor.execute_test_suite(test_suite, scenario_jars.base)
            logging.info("Starting execution of %s test suite in left", test_suite.generator_name)
            results_left = self._test_suite_executor.execute_test_suite(test_suite, scenario_jars.left)
            logging.info("Starting execution of %s test suite in right", test_suite.generator_name)
            results_right = self._test_suite_executor.execute_test_suite(test_suite, scenario_jars.right)
            logging.info("Starting execution of %s test suite in merge", test_suite.generator_name)
            results_merge = self._test_suite_executor.execute_test_suite(test_suite, scenario_jars.merge)

            test_results = self._merge_test_case_results(test_suite, results_base, results_left, results_right, results_merge)
            results += test_results

        return results

    def _merge_test_case_results(self, test_suite: TestSuite, results_base: Dict[str, TestCaseResult], results_left: Dict[str, TestCaseResult], results_right: Dict[str, TestCaseResult], results_merge: Dict[str, TestCaseResult]) -> List[TestCaseExecutionInMergeScenario]:
        test_cases = results_base.keys()
        test_suite_results: List[TestCaseExecutionInMergeScenario] = list()

        for test_case in test_cases:
            test_suite_results.append(
                TestCaseExecutionInMergeScenario(
                    test_suite,
                    test_case,
                    results_base.get(test_case, TestCaseResult.NOT_EXECUTABLE),
                    results_left.get(test_case, TestCaseResult.NOT_EXECUTABLE),
                    results_right.get(test_case, TestCaseResult.NOT_EXECUTABLE),
                    results_merge.get(test_case, TestCaseResult.NOT_EXECUTABLE)
                )
            )

        return test_suite_results

    def execute_test_suite_with_coverage(self, test_suite: TestSuite, target_jar: str, test_cases: List[str], watched_classes: List[str]) -> str:

        pass
