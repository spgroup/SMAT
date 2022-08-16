from typing import Dict, List

from nimrod.test_suite_generation.generators.test_suite_generator import TestSuiteGenerator
from nimrod.test_suite_generation.test_suite import TestSuite


class TestSuiteGeneration:
    _testSuiteGenerators: List[TestSuiteGenerator]

    def __init__(self, testSuiteGenerators: List[TestSuiteGenerator]) -> None:
        self._testSuiteGenerators = testSuiteGenerators

    def generateTestSuites(self, project: str, commit: str, inputJar: str, targets: "Dict[str, List[str]]") -> List[TestSuite]:
        testSuites: List[TestSuite] = list()

        for generator in self._testSuiteGenerators:
            outputPath = project + inputJar + commit
            testSuite = generator.generateTestSuite(inputJar, outputPath, targets)
            testSuites.append(testSuite)

        return testSuites
