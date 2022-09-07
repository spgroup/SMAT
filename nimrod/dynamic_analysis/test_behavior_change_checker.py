from unittest import TestCase

from nimrod.dynamic_analysis.behavior_change_checker import \
    BehaviorChangeChecker
from nimrod.test_suites_execution.test_case_result import TestCaseResult


class TestBehaviorChangeChecker(TestCase):
  def get_bcc(self):
    return BehaviorChangeChecker()

  def test_there_is_a_behavior_change_if_it_fails_in_one_and_passes_in_the_other(self):
    self.assertTrue(self.get_bcc().has_behavior_change_between(
        TestCaseResult.FAIL, TestCaseResult.PASS))
    self.assertTrue(self.get_bcc().has_behavior_change_between(
        TestCaseResult.PASS, TestCaseResult.FAIL))

  def test_there_is_not_a_behavior_change_if_either_one_of_the_tests_is_not_executable(self):
    self.assertFalse(self.get_bcc().has_behavior_change_between(
        TestCaseResult.FAIL, TestCaseResult.NOT_EXECUTABLE))
    self.assertFalse(self.get_bcc().has_behavior_change_between(
        TestCaseResult.NOT_EXECUTABLE, TestCaseResult.FAIL))

    self.assertFalse(self.get_bcc().has_behavior_change_between(
        TestCaseResult.PASS, TestCaseResult.NOT_EXECUTABLE))
    self.assertFalse(self.get_bcc().has_behavior_change_between(
        TestCaseResult.NOT_EXECUTABLE, TestCaseResult.PASS))

  def test_there_is_not_a_behavior_change_if_either_one_of_the_tests_is_flaky(self):
    self.assertFalse(self.get_bcc().has_behavior_change_between(
        TestCaseResult.FAIL, TestCaseResult.FLAKY))
    self.assertFalse(self.get_bcc().has_behavior_change_between(
        TestCaseResult.FLAKY, TestCaseResult.FAIL))

    self.assertFalse(self.get_bcc().has_behavior_change_between(
        TestCaseResult.PASS, TestCaseResult.FLAKY))
    self.assertFalse(self.get_bcc().has_behavior_change_between(
        TestCaseResult.FLAKY, TestCaseResult.PASS))
