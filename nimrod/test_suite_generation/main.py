import logging
from typing import List

from nimrod.test_suite_generation.generators.test_suite_generator import TestSuiteGenerator
from nimrod.test_suite_generation.test_suite import TestSuite
from nimrod.input_parsing.smat_input import SmatInput


class TestSuiteGeneration:
    def __init__(self, test_suite_generators: List[TestSuiteGenerator]) -> None:
        self._test_suite_generators = test_suite_generators

    def generate_test_suites(self, scenario: SmatInput, input_jar: str) -> List[TestSuite]:
        logging.info("Starting tests generation for project %s using jar %s", scenario.project_name, input_jar)
        test_suites: List[TestSuite] = list()

        for generator in self._test_suite_generators:
            try:
                test_suites.append(generator.generate_and_compile_test_suite(scenario, input_jar))
            except Exception as error:
                logging.error(f"It was not possible to generate test suite using {generator.get_generator_tool_name()}")
                logging.debug(error)

        logging.info("Finished tests generation for project %s using jar %s", scenario.project_name, input_jar)
        return test_suites
