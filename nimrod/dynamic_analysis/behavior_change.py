from typing import Tuple
from nimrod.test_suites_execution.test_case_execution_in_merge_scenario import TestCaseExecutionInMergeScenario


class BehaviorChange:
    def __init__(self, detected_in: TestCaseExecutionInMergeScenario, between: Tuple[str, str]):
        self.detected_in = detected_in
        self.between = between
