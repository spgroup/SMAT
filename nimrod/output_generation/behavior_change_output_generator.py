from typing import Dict, List, Tuple, TypedDict
from nimrod.output_generation.output_generator import OutputGenerator, OutputGeneratorContext


class BehaviorChangeOutput(TypedDict):
    project_name: str
    scenario_commits: Dict[str, str]
    test_case_name: str
    test_case_results: Dict[str, str]
    test_suite_path: str
    between: Tuple[str, str]


class BehaviorChangeOutputGenerator(OutputGenerator[List[BehaviorChangeOutput]]):
    def __init__(self) -> None:
        super().__init__("behavior_changes")

    def _generate_report_data(self, context: OutputGeneratorContext) -> List[BehaviorChangeOutput]:
        report_data: List[BehaviorChangeOutput] = list()

        for behavior_change in context.behavior_changes:
            report_data.append({
                "project_name": context.scenario.project_name,
                "scenario_commits": context.scenario.scenario_commits.__dict__,
                "test_case_name": behavior_change.detected_in.name,
                "test_case_results": {
                    "base": behavior_change.detected_in.base,
                    "left": behavior_change.detected_in.left,
                    "right": behavior_change.detected_in.right,
                    "merge": behavior_change.detected_in.merge
                },
                "test_suite_path": behavior_change.detected_in.test_suite.path,
                "between": behavior_change.between
            })

        return report_data
