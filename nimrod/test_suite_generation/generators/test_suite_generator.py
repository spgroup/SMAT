
from abc import ABC, abstractmethod
from typing import Dict, List

from nimrod.test_suite_generation.test_suite import TestSuite


class TestSuiteGenerator(ABC):
    @abstractmethod
    def get_generator_name(self) -> str:
        pass

    @abstractmethod
    def generate_test_suite(self, input_jar: str, output_path: str, targets: "Dict[str, List[str]]") -> TestSuite:
        pass
