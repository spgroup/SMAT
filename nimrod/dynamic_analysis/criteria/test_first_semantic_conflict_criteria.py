from unittest import TestCase

from nimrod.dynamic_analysis.criteria.first_semantic_conflict_criteria import \
    FirstSemanticConflictCriteria
from nimrod.test_suites_execution.test_case_execution_in_merge_scenario import \
    TestCaseExecutionInMergeScenario
from nimrod.test_suites_execution.test_case_result import TestCaseResult


class TestFirstSemanticConflictCriteria(TestCase):
    def test_is_satisfied_if_it_passes_in_base_and_merge_but_fails_in_a_single_parent(self):
        scenario = TestCaseExecutionInMergeScenario(
            test_suite=None,
            name="test001",
            base=TestCaseResult.PASS,
            merge=TestCaseResult.PASS,
            left=TestCaseResult.FAIL,
            right=TestCaseResult.NOT_EXECUTABLE
        )

        self.assertTrue(FirstSemanticConflictCriteria().is_satisfied_by(scenario))

    def test_is_satisfied_if_it_fails_in_base_and_merge_but_passes_in_a_single_parent(self):
        scenario = TestCaseExecutionInMergeScenario(
            test_suite=None,
            name="test001",
            base=TestCaseResult.FAIL,
            merge=TestCaseResult.FAIL,
            left=TestCaseResult.NOT_EXECUTABLE,
            right=TestCaseResult.PASS
        )

        self.assertTrue(FirstSemanticConflictCriteria().is_satisfied_by(scenario))
