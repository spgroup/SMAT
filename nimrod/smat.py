from typing import List
from nimrod.dynamic_analysis.main import DynamicAnalysis
from nimrod.input_parsing.smat_input import SmatInput
from nimrod.test_suite_generation.main import TestSuiteGeneration
from nimrod.test_suite_generation.test_suite import TestSuite
from nimrod.test_suites_execution.main import TestSuitesExecution


class SMAT:
  def __init__(self, test_suite_generation: TestSuiteGeneration, test_suites_execution: TestSuitesExecution, dynamic_analisys: DynamicAnalysis) -> None:
    self._test_suite_generation = test_suite_generation
    self._test_suites_execution = test_suites_execution
    self._dynamic_analysis = dynamic_analisys

  def run_tool_for_semmantic_conflict_detection(self, scenario: SmatInput) -> None:
    test_suites = self._generate_test_suites_for_scenario(scenario)
    executions = self._test_suites_execution.execute_test_suites(test_suites, scenario.scenario_jars)
    semantic_conflicts = self._dynamic_analysis.check_for_semantic_conflicts(executions)    
  
  def _generate_test_suites_for_scenario(self, scenario: SmatInput) -> List[TestSuite]:
      suites_left = self._test_suite_generation.generate_test_suites(scenario, scenario.scenario_jars.left)
      suites_right = self._test_suite_generation.generate_test_suites(scenario, scenario.scenario_jars.right)

      return suites_left + suites_right




