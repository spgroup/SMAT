from nimrod.test_suites_execution.test_case_result import TestCaseResult


class TestCaseExecutionInMergeScenario:
    def __init__(self, name: str, base: TestCaseResult, left: TestCaseResult, right: TestCaseResult, merge: TestCaseResult):
      self.name = name
      self.base = base
      self.left = left
      self.right = right
      self.merge = merge
