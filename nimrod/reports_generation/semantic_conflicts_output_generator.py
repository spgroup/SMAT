from nimrod.reports_generation.output_generator import OutputGenerator
from nimrod.test_suites_execution.main import TestSuitesExecution


class SemanticConflictsOutputGenerator(OutputGenerator):
    def __init__(self, test_suites_execution: TestSuitesExecution) -> None:
        super().__init__("semantic_conflicts.csv")
        self._test_suites_execution = test_suites_execution

    def _generate_report_data(self, context):
        return super()._generate_report_data(context)
