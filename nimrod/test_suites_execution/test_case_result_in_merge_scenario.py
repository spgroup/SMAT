from nimrod.test_suites_execution.test_case_result import TestCaseResult


class TestCaseResultInMergeScenario:
    def __init__(self, base: TestCaseResult, left: TestCaseResult, right: TestCaseResult, merge: TestCaseResult):
      self.base = base
      self.left = left
      self.right = right
      self.merge = merge
