from nimrod.dynamic_analysis.criteria.dynamic_analysis_criteria import \
    DynamicAnalysisCriteria
from nimrod.test_suites_execution.test_case_execution_in_merge_scenario import \
    TestCaseExecutionInMergeScenario
from nimrod.test_suites_execution.test_case_result import TestCaseResult


class SecondSemanticConflictCriteria(DynamicAnalysisCriteria):
  def is_satisfied_by(self, test_case_execution: TestCaseExecutionInMergeScenario) -> bool:
    fails_in_base_and_both_parents_but_passes_in_merge = \
        test_case_execution.base == TestCaseResult.FAIL \
        and test_case_execution.left == TestCaseResult.FAIL \
        and test_case_execution.right == TestCaseResult.FAIL \
        and test_case_execution.merge == TestCaseResult.PASS

    passes_in_base_and_both_parents_but_fails_in_merge = \
        test_case_execution.base == TestCaseResult.PASS \
        and test_case_execution.left == TestCaseResult.PASS \
        and test_case_execution.right == TestCaseResult.PASS \
        and test_case_execution.merge == TestCaseResult.FAIL

    return fails_in_base_and_both_parents_but_passes_in_merge or passes_in_base_and_both_parents_but_fails_in_merge
