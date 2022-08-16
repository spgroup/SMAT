import logging
from os import path
from typing import Dict, List

from nimrod.test_suite_generation.generators.test_suite_generator import TestSuiteGenerator
from nimrod.test_suite_generation.test_suite import TestSuite
from nimrod.tests.utils import get_base_output_path


class TestSuiteGeneration:
    def __init__(self, test_suite_generators: List[TestSuiteGenerator]) -> None:
        self._test_suite_generators = test_suite_generators

    def generate_test_suites(self, project: str, commit: str, input_jar: str, targets: "Dict[str, List[str]]") -> List[TestSuite]:
        logging.info("Starting tests generation for project %s commit %s with jar %s", project, commit, input_jar)
        test_suites: List[TestSuite] = list()

        for generator in self._test_suite_generators:
            output_path = path.join(get_base_output_path(), project, commit, generator.get_generator_tool_name())
            tests_class_path = generator.generate_and_compile_test_suite(input_jar, output_path, targets)

            test_suites.append(TestSuite(
                generator_name=generator.get_generator_tool_name(),
                commit=commit,
                project=project,
                path=output_path,
                class_path=tests_class_path,
            ))

        logging.info("Finished tests generation for project %s commit %s with jar %s", project, commit, input_jar)
        return test_suites
