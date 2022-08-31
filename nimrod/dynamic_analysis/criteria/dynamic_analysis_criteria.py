from abc import ABC, abstractmethod

from nimrod.test_suites_execution.test_case_execution_in_merge_scenario import \
    TestCaseExecutionInMergeScenario


class DynamicAnalysisCriteria(ABC):
  @abstractmethod
  def is_satisfied_by(self, test_case_execution: TestCaseExecutionInMergeScenario) -> bool:
    pass
