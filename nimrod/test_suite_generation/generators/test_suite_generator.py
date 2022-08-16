
from abc import ABC, abstractmethod
from typing import Dict, List

from nimrod.test_suite_generation.test_suite import TestSuite


class TestSuiteGenerator(ABC):
    @abstractmethod
    def generateTestSuite(self, inputJar: str, outputPath: str, targets: "Dict[str, List[str]]") -> TestSuite:
        pass
