from typing import Dict, List

from nimrod.test_suite_generation.generators.test_suite_generator import TestSuiteGenerator
from nimrod.test_suite_generation.test_suite import TestSuite


class TestSuiteGeneration:
    _test_suite_generators: List[TestSuiteGenerator]

    def __init__(self, test_suite_generators: List[TestSuiteGenerator]) -> None:
        self._test_suite_generators = test_suite_generators

    def generate_test_suites(self, project: str, commit: str, input_jar: str, targets: "Dict[str, List[str]]") -> List[TestSuite]:
        test_suites: List[TestSuite] = list()

        for generator in self._test_suite_generators:
            output_path = project + input_jar + commit
            test_suite = generator.generate_test_suite(input_jar, output_path, targets)
            test_suites.append(test_suite)

        return test_suites
