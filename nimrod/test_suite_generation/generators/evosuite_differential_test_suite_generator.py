import logging
from nimrod.core.merge_scenario_under_analysis import MergeScenarioUnderAnalysis

from nimrod.test_suite_generation.generators.evosuite_test_suite_generator import EvosuiteTestSuiteGenerator
from nimrod.tools.bin import EVOSUITE


class EvosuiteDifferentialTestSuiteGenerator(EvosuiteTestSuiteGenerator):
    def get_generator_tool_name(self) -> str:
        return "EVOSUITE_DIFFERENTIAL"

    def _execute_tool_for_tests_generation(self, input_jar: str, output_path: str, scenario: MergeScenarioUnderAnalysis, use_determinism: bool) -> None:
        for class_name, methods in scenario.targets.items():
          logging.debug(f"Starting generation for class {class_name}")
          params = [
              '-jar', EVOSUITE,
              '-regressionSuite',
              '-projectCP', input_jar,
              f'-Dregressioncp={scenario.scenario_jars.base}',
              '-class', class_name,
              '-DOUTPUT_DIR=' + output_path,
              '-Dminimize=false',
              '-Djunit_check=false',
              '-Dinline=false',
          ]
          
          if use_determinism:
            params += ["-Dstopping_condition=MaxTests",
                       f"-seed={self.SEED}", f'-Dsearch_budget={self.DETERMINISTIC_TESTS_QUANTITY}']
          else:
            params += [f'-Dsearch_budget={self.SEARCH_TIME_AVAILABLE}']

          if(len(methods) > 0):
            params.append(
                f'-Dtarget_method_list="{self._create_method_list(methods)}"')

          self._java.exec_java(output_path, self._java.get_env(), 3000, *tuple(params))
