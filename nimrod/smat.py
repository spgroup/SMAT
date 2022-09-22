from typing import List

from nimrod.dynamic_analysis.main import DynamicAnalysis
from nimrod.input_parsing.smat_input import SmatInput
from nimrod.reports_generation.output_generator import OutputGenerator
from nimrod.test_suite_generation.main import TestSuiteGeneration
from nimrod.test_suite_generation.test_suite import TestSuite
from nimrod.test_suites_execution.main import TestSuitesExecution


class SMAT:
  def __init__(self, test_suite_generation: TestSuiteGeneration, test_suites_execution: TestSuitesExecution, dynamic_analisys: DynamicAnalysis, output_generators: List[OutputGenerator]) -> None:
    self._test_suite_generation = test_suite_generation
    self._test_suites_execution = test_suites_execution
    self._dynamic_analysis = dynamic_analisys
    self._output_generators = output_generators

  def run_tool_for_semmantic_conflict_detection(self, scenario: SmatInput) -> None:
    test_suites = self._generate_test_suites_for_scenario(scenario)
    executions = self._test_suites_execution.execute_test_suites(test_suites, scenario.scenario_jars)
    semantic_conflicts = self._dynamic_analysis.check_for_semantic_conflicts(executions)    
    behavior_changes = self._dynamic_analysis.check_for_behavior_changes(executions)
    for output_generator in self._output_generators:
      output_generator.write_report(scenario, semantic_conflicts)
  
  def _generate_test_suites_for_scenario(self, scenario: SmatInput) -> List[TestSuite]:
      suites_left = self._test_suite_generation.generate_test_suites(scenario, scenario.scenario_jars.left, True)
      suites_right = self._test_suite_generation.generate_test_suites(scenario, scenario.scenario_jars.right, True)

      return suites_left + suites_right
