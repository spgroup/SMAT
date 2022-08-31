from typing import List
from nimrod.dynamic_analysis.criteria.dynamic_analysis_criteria import DynamicAnalysisCriteria
from nimrod.dynamic_analysis.semantic_conflict import SemanticConflict
from nimrod.test_suites_execution.test_case_execution_in_merge_scenario import TestCaseExecutionInMergeScenario


class DynamicAnalysis:
    def __init__(self, semantic_conflict_criterias: List[DynamicAnalysisCriteria]):
        self._semantic_conflict_criterias = semantic_conflict_criterias

    def check_for_semantic_conflicts(self, test_case_executions: List[TestCaseExecutionInMergeScenario]):
        conflicts = []

        for test_case_execution in test_case_executions:
            for criteria in self._semantic_conflict_criterias:
                if criteria.is_satisfied_by(test_case_execution):
                    conflicts.append(SemanticConflict(
                        satisfying_criteria=criteria,
                        detected_in=test_case_execution
                    ))

        return conflicts
