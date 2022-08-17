import logging
import os
from typing import Dict, List
from nimrod.input_parsing.smat_input import SmatInput

from nimrod.test_suite_generation.generators.evosuite_test_suite_generator import EvosuiteTestSuiteGenerator
from nimrod.tools.bin import EVOSUITE, EVOSUITE_RUNTIME


class EvosuiteDifferentialTestSuiteGenerator(EvosuiteTestSuiteGenerator):
    def get_generator_tool_name(self) -> str:
        return "EVOSUITE_DIFFERENTIAL"

    def _execute_tool_for_tests_generation(self, input_jar: str, output_path: str, scenario: SmatInput) -> None:
        for class_name, methods in scenario.targets.items():
          logging.debug(f"Starting generation for class {class_name}")
          params = [
              '-jar', EVOSUITE,
              '-regressionSuite',
              '-projectCP', input_jar,
              f'-Dregressioncp={scenario.scenario_jars.base}',
              '-class', class_name,
              f'-Dsearch_budget={self.SEARCH_BUDGET}',
              '-DOUTPUT_DIR=' + output_path,
          ]

          if(len(methods) > 0):
            params.append(
                f'-Dtarget_method_list="{self._create_method_list(methods)}"')

          self._java.exec_java(output_path, self._java.get_env(), 3000, *tuple(params))
