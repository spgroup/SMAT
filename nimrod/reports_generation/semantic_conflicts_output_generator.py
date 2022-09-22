from typing import Dict, List
from nimrod.dynamic_analysis.semantic_conflict import SemanticConflict
from nimrod.input_parsing.smat_input import SmatInput
from nimrod.reports_generation.output_generator import OutputGenerator
from nimrod.test_suites_execution.main import TestSuitesExecution


class SemanticConflictsOutput:
    def __init__(self, project_name: str, scenario_commits: Dict[str, str], criteria: str, test_case_name: str, test_case_results: Dict[str, str], test_suite_path: str, exercised_targets: Dict[str, List[str]]) -> None:
        self.project_name = project_name
        self.scenario_commits = scenario_commits
        self.criteria = criteria
        self.test_case_name = test_case_name
        self.test_case_results = test_case_results
        self.test_suite_path = test_suite_path
        self.exercised_targets = exercised_targets

class SemanticConflictsOutputGenerator(OutputGenerator):
    def __init__(self, test_suites_execution: TestSuitesExecution) -> None:
        super().__init__("semantic_conflicts")
        self._test_suites_execution = test_suites_execution

    def _generate_report_data(self, scenario: SmatInput, semantic_conflicts: List[SemanticConflict]):
        report_data: List[SemanticConflictsOutput] = list()

        for semantic_conflict in semantic_conflicts:
            # We need to detect which targets from the input were exercised in this conflict.
            coverage_report_path = self._test_suites_execution.execute_test_suite_with_coverage(
                test_suite=semantic_conflict._detected_in.test_suite,
                target_jar=scenario.scenario_jars.merge,
                test_cases=[semantic_conflict._detected_in.name],
                watched_classes=list(scenario.targets.keys())
            )

            exercised_targets = self._extract_exercised_targets_from_coverage_report(
                coverage_report_path=coverage_report_path,
                targets=scenario.targets
            )
        
        return report_data

    def _extract_exercised_targets_from_coverage_report(self, coverage_report_path: str, targets: Dict[str, List[str]]):
        pass
