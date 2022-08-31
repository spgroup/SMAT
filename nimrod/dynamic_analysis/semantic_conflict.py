
from nimrod.dynamic_analysis.criteria.dynamic_analysis_criteria import DynamicAnalysisCriteria
from nimrod.test_suites_execution.test_case_execution_in_merge_scenario import TestCaseExecutionInMergeScenario


class SemanticConflict:
    def __init__(self, satisfying_criteria: DynamicAnalysisCriteria, detected_in: TestCaseExecutionInMergeScenario) -> None:
        self._satisfying_criteria = satisfying_criteria
        self._detected_in = detected_in
