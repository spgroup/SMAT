import logging
from typing import Dict, List

from nimrod.test_suite_generation.generators.test_suite_generator import \
    TestSuiteGenerator
from nimrod.test_suite_generation.test_suite import TestSuite


class TestSuiteGeneration:
    def __init__(self, test_suite_generators: List[TestSuiteGenerator]) -> None:
        self._test_suite_generators = test_suite_generators

    def generate_test_suites(self, project: str, commit: str, input_jar: str, targets: "Dict[str, List[str]]") -> List[TestSuite]:
        logging.info("Starting tests generation for project %s commit %s with jar %s", project, commit, input_jar)
        test_suites: List[TestSuite] = list()

        for generator in self._test_suite_generators:
            try:
                test_suites.append(generator.generate_and_compile_test_suite(project, commit, input_jar, targets))
            except:
                logging.error(f"It was not possible to generate test suite using {generator.get_generator_tool_name()}")

        logging.info("Finished tests generation for project %s commit %s with jar %s", project, commit, input_jar)
        return test_suites
