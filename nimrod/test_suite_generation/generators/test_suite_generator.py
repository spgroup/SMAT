
from abc import ABC, abstractmethod
import logging
from os import makedirs, path
from typing import Dict, List
from nimrod.tools.bin import HAMCREST, JUNIT

from nimrod.tools.java import Java
from nimrod.utils import generate_classpath


class TestSuiteGenerator(ABC):
    def __init__(self, java: Java) -> None:
        self._java = java

    def generate_and_compile_test_suite(self, input_jar: str, output_path: str, targets: "Dict[str, List[str]]") -> List[str]:
        makedirs(output_path, exist_ok=True)
        makedirs(path.join(output_path, "classes"), exist_ok=True)

        logging.info(f"Starting generation with {self.get_generator_tool_name()}")
        params = self._get_tool_parameters_for_tests_generation(input_jar, output_path, targets)
        self._java.exec_java(output_path, self._java.get_env(), 3000, *tuple(params))
        logging.info(f"Finished generation with {self.get_generator_tool_name()}")

        logging.info(f"Starting compilation for suite generated with {self.get_generator_tool_name()}")
        tests_class_path = self._compile_test_suite(input_jar, output_path)
        logging.info(f"Finished compilation for suite generated with {self.get_generator_tool_name()}")

        return tests_class_path

    @abstractmethod
    def get_generator_tool_name(self) -> str:
        pass

    @abstractmethod
    def _get_tool_parameters_for_tests_generation(self, input_jar: str, output_path: str, targets: "Dict[str, List[str]]") -> List[str]:
        pass

    def _compile_test_suite(self, input_jar: str, output_path: str) -> List[str]:
        compiled_classes = path.join(output_path, 'classes')
        class_path = generate_classpath([input_jar, output_path, compiled_classes, JUNIT, HAMCREST])
        self._java.compile_all(class_path, output_path)
        return class_path
