from operator import xor

from nimrod.dynamic_analysis.criteria.dynamic_analysis_criteria import \
    DynamicAnalysisCriteria
from nimrod.test_suites_execution.test_case_execution_in_merge_scenario import \
    TestCaseExecutionInMergeScenario
from nimrod.test_suites_execution.test_case_result import TestCaseResult


class FirstSemanticConflictCriteria(DynamicAnalysisCriteria):
    def is_satisfied_by(self, test_case_execution: TestCaseExecutionInMergeScenario) -> bool:
        passes_in_base_and_merge_but_fails_in_a_single_parent = \
            test_case_execution.merge == TestCaseResult.PASS \
            and test_case_execution.base == TestCaseResult.PASS \
            and bool(xor(test_case_execution.left == TestCaseResult.FAIL, test_case_execution.right == TestCaseResult.FAIL))

        return passes_in_base_and_merge_but_fails_in_a_single_parent
