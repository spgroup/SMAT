from typing import List
from nimrod.dynamic_analysis.behavior_change import BehaviorChange
from nimrod.dynamic_analysis.behavior_change_checker import BehaviorChangeChecker
from nimrod.dynamic_analysis.criteria.dynamic_analysis_criteria import DynamicAnalysisCriteria
from nimrod.dynamic_analysis.semantic_conflict import SemanticConflict
from nimrod.test_suites_execution.test_case_execution_in_merge_scenario import TestCaseExecutionInMergeScenario


class DynamicAnalysis:
    def __init__(self, semantic_conflict_criterias: List[DynamicAnalysisCriteria], behavior_change_checker: BehaviorChangeChecker):
        self._semantic_conflict_criterias = semantic_conflict_criterias
        self._behavior_change_checker = behavior_change_checker

    def check_for_semantic_conflicts(self, test_case_executions: List[TestCaseExecutionInMergeScenario]) -> List[SemanticConflict]:
        conflicts = []

        for test_case_execution in test_case_executions:
            for criteria in self._semantic_conflict_criterias:
                if criteria.is_satisfied_by(test_case_execution):
                    conflicts.append(SemanticConflict(
                        satisfying_criteria=criteria,
                        detected_in=test_case_execution
                    ))

        return conflicts

    def check_for_behavior_changes(self, test_case_executions: List[TestCaseExecutionInMergeScenario]) -> List[BehaviorChange]:
        behavior_changes = []

        for execution in test_case_executions:
            if self._behavior_change_checker.has_behavior_change_between(execution.base, execution.left):
                behavior_changes.append(BehaviorChange(execution, ("BASE", "LEFT")))
            if self._behavior_change_checker.has_behavior_change_between(execution.base, execution.right):
                behavior_changes.append(BehaviorChange(execution, ("BASE", "RIGHT")))
            if self._behavior_change_checker.has_behavior_change_between(execution.left, execution.merge):
                behavior_changes.append(BehaviorChange(execution, ("LEFT", "MERGE")))
            if self._behavior_change_checker.has_behavior_change_between(execution.right, execution.merge):
                behavior_changes.append(BehaviorChange(execution, ("RIGHT", "MERGE")))

        return behavior_changes
