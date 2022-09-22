from typing import List

from nimrod.dynamic_analysis.behavior_change import BehaviorChange
from nimrod.dynamic_analysis.semantic_conflict import SemanticConflict
from nimrod.core.merge_scenario_under_analysis import MergeScenarioUnderAnalysis
from nimrod.test_suite_generation.test_suite import TestSuite
from nimrod.test_suites_execution.test_case_execution_in_merge_scenario import \
    TestCaseExecutionInMergeScenario


class OutputGeneratorContext:
    def __init__(self,
                 scenario: MergeScenarioUnderAnalysis,
                 test_suites: List[TestSuite],
                 test_case_executions: List[TestCaseExecutionInMergeScenario],
                 semantic_conflicts: List[SemanticConflict],
                 behavior_changes: List[BehaviorChange]) -> None:
        self._scenario = scenario
        self._test_suites = test_suites
        self._test_case_executions = test_case_executions
        self._semantic_conflicts = semantic_conflicts
        self._behavior_changes = behavior_changes

    @property
    def scenario(self) -> MergeScenarioUnderAnalysis:
        return self._scenario

    @property
    def test_suites(self) -> List[TestSuite]:
        return self._test_suites

    @property
    def test_case_executions(self) -> List[TestCaseExecutionInMergeScenario]:
        return self._test_case_executions

    @property
    def semantic_conflicts(self) -> List[SemanticConflict]:
        return self._semantic_conflicts

    @property
    def behavior_changes(self) -> List[BehaviorChange]:
        return self._behavior_changes
