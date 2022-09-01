from nimrod.test_suite_generation.test_suite import TestSuite
from nimrod.test_suites_execution.test_case_result import TestCaseResult


class TestCaseExecutionInMergeScenario():
    __test__ = False

    def __init__(self, test_suite: TestSuite, name: str, base: TestCaseResult, left: TestCaseResult, right: TestCaseResult, merge: TestCaseResult):
      self.test_suite = test_suite
      self.name = name
      self.base = base
      self.left = left
      self.right = right
      self.merge = merge
