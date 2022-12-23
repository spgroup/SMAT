from nimrod.test_suites_execution.test_case_result import TestCaseResult


class BehaviorChangeChecker:
    def has_behavior_change_between(self, one: TestCaseResult, two: TestCaseResult) -> bool:
      if one == TestCaseResult.PASS:
          return two == TestCaseResult.FAIL
      elif one == TestCaseResult.FAIL:
          return two == TestCaseResult.PASS
      return False
