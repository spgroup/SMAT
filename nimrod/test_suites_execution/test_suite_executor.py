from typing import Dict
from nimrod.test_suite_generation.test_suite import TestSuite
from nimrod.test_suites_execution.test_case_result import TestCaseResult


class TestSuiteExecutor:
    def execute_test_suite(self, test_suite: TestSuite, jar: str) -> Dict[str, TestCaseResult]:
        return dict()
