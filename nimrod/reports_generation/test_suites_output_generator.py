from typing import List, TypedDict
from nimrod.dynamic_analysis.behavior_change import BehaviorChange
from nimrod.dynamic_analysis.semantic_conflict import SemanticConflict
from nimrod.reports_generation.output_generator import OutputGenerator, OutputGeneratorContext
from nimrod.test_suite_generation.test_suite import TestSuite


class TestSuitesOutput(TypedDict):
    project_name: str
    generator_name: str
    path: str
    detected_semantic_conflicts: bool
    detected_behavior_changes_between_pairs: bool


class TestSuitesOutputGenerator(OutputGenerator[List[TestSuitesOutput]]):
    def __init__(self) -> None:
        super().__init__("test_suites")

    def _generate_report_data(self, context: OutputGeneratorContext) -> List[TestSuitesOutput]:
        report_data: List[TestSuitesOutput] = list()

        for test_suite in context.test_suites:
            report_data.append({
                "project_name": context.scenario.project_name,
                "generator_name": test_suite.generator_name,
                "path": test_suite.path,
                "detected_semantic_conflicts": self._has_detected_semantic_conflicts_in_test_suite(test_suite, context.semantic_conflicts),
                "detected_behavior_changes_between_pairs": self._has_detected_behavior_changes_in_test_suite(test_suite, context.behavior_changes)
            })

        return report_data

    def _has_detected_semantic_conflicts_in_test_suite(self, test_suite: TestSuite, semantic_conflicts: List[SemanticConflict]):
      for semantic_conflict in semantic_conflicts:
        if semantic_conflict.detected_in.test_suite == test_suite:
          return True
      return False

    def _has_detected_behavior_changes_in_test_suite(self, test_suite: TestSuite, behavior_changes: List[BehaviorChange]):
      for behavior_change in behavior_changes:
        if behavior_change.detected_in.test_suite == test_suite:
          return True
      return False
