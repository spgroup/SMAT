from typing import Dict, List, TypedDict
from nimrod.dynamic_analysis.semantic_conflict import SemanticConflict
from nimrod.input_parsing.smat_input import SmatInput
from nimrod.reports_generation.output_generator import OutputGenerator
from nimrod.test_suites_execution.main import TestSuitesExecution
from os import path
from bs4 import BeautifulSoup


class SemanticConflictsOutput(TypedDict):
    project_name: str
    scenario_commits: Dict[str, str]
    criteria: str
    test_case_name: str
    test_case_results: Dict[str, str]
    test_suite_path: str
    scenario_targets: Dict[str, List[str]]
    exercised_targets: Dict[str, List[str]]


class SemanticConflictsOutputGenerator(OutputGenerator[List[SemanticConflictsOutput]]):
    def __init__(self, test_suites_execution: TestSuitesExecution) -> None:
        super().__init__("semantic_conflicts")
        self._test_suites_execution = test_suites_execution

    def _generate_report_data(self, scenario: SmatInput, semantic_conflicts: List[SemanticConflict]) -> List[SemanticConflictsOutput]:
        report_data: List[SemanticConflictsOutput] = list()

        for semantic_conflict in semantic_conflicts:
            # We need to detect which targets from the input were exercised in this conflict.
            coverage_report_root = self._test_suites_execution.execute_test_suite_with_coverage(
                test_suite=semantic_conflict._detected_in.test_suite,
                target_jar=scenario.scenario_jars.merge,
                test_cases=[semantic_conflict._detected_in.name]
            )

            exercised_targets = self._extract_exercised_targets_from_coverage_report(
                coverage_report_root=coverage_report_root,
                targets=scenario.targets
            )

            report_data.append({
                "project_name": scenario.project_name,
                "scenario_commits": {
                    "base": scenario.scenario_commits.base,
                    "left": scenario.scenario_commits.left,
                    "right": scenario.scenario_commits.right,
                    "merge": scenario.scenario_commits.merge
                },
                "criteria": semantic_conflict._satisfying_criteria.__class__.__name__,
                "test_case_name": semantic_conflict._detected_in.name,
                "test_case_results": {
                    "base": semantic_conflict._detected_in.base,
                    "left": semantic_conflict._detected_in.left,
                    "right": semantic_conflict._detected_in.right,
                    "merge": semantic_conflict._detected_in.merge
                },
                "test_suite_path": semantic_conflict._detected_in.test_suite.path,
                "scenario_targets": scenario.targets,
                "exercised_targets": exercised_targets
            })

        return report_data

    def _extract_exercised_targets_from_coverage_report(self, coverage_report_root: str, targets: Dict[str, List[str]]):
        exercised_targets: Dict[str, List[str]] = dict()

        for class_name in targets.keys():
            for method_name in targets[class_name]:
                if self._was_target_exercised(coverage_report_root, class_name, method_name):
                    exercised_targets[class_name] = exercised_targets.get(
                        class_name, []) + [method_name]

        return exercised_targets

    def _was_target_exercised(self, coverage_report_root: str, fqcn: str, method_signature: str) -> bool:
        [package_name, class_name] = fqcn.rsplit('.', 1)
        class_report_path = path.join(
            coverage_report_root, package_name, f"{class_name}.html")

        method_name = method_signature[:method_signature.index("(") + 1]

        report_file = open(class_report_path)
        decoded_report = BeautifulSoup(report_file, 'html.parser')
        method_report_rows = decoded_report.select("#coveragetable > tbody > tr")

        # We itereate in each method row
        for method_row in method_report_rows:
            if method_row.get_text().find(method_name) != -1:
                if method_row.select_one('td:nth-last-child(2)').get_text() == '0':
                    return True

        return False
