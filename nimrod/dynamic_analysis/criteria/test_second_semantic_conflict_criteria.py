from unittest import TestCase

from nimrod.dynamic_analysis.criteria.second_semantic_conflict_criteria import \
    SecondSemanticConflictCriteria
from nimrod.test_suites_execution.test_case_execution_in_merge_scenario import \
    TestCaseExecutionInMergeScenario
from nimrod.test_suites_execution.test_case_result import TestCaseResult


class TestSecondSemanticConflictCriteria(TestCase):
  def test_is_satisfied_if_it_fails_in_base_and_in_both_parents_but_passes_in_merge(self):
    scenario = TestCaseExecutionInMergeScenario(
        test_suite=None,
        name="test001",
        base=TestCaseResult.FAIL,
        left=TestCaseResult.FAIL,
        right=TestCaseResult.FAIL,
        merge=TestCaseResult.PASS,
    )

    self.assertTrue(SecondSemanticConflictCriteria().is_satisfied_by(scenario))

  def test_is_satisfied_if_it_passes_in_base_and_in_both_parents_but_fails_in_merge(self):
    scenario = TestCaseExecutionInMergeScenario(
        test_suite=None,
        name="test001",
        base=TestCaseResult.PASS,
        left=TestCaseResult.PASS,
        right=TestCaseResult.PASS,
        merge=TestCaseResult.FAIL,
    )

    self.assertTrue(SecondSemanticConflictCriteria().is_satisfied_by(scenario))
