import json
from abc import ABC, abstractmethod
import logging
from os import makedirs, path
from typing import TypeVar, Generic

from nimrod.output_generation.output_generator_context import OutputGeneratorContext
from nimrod.tests.utils import get_base_output_path

T = TypeVar("T")


class OutputGenerator(ABC, Generic[T]):
    REPORTS_DIRECTORY = path.join(get_base_output_path(), "reports")

    def __init__(self, report_name: str) -> None:
        super().__init__()
        makedirs(self.REPORTS_DIRECTORY, exist_ok=True)
        self._report_name = report_name + ".json"

    @abstractmethod
    def _generate_report_data(self, context: OutputGeneratorContext) -> T:
        pass

    def write_report(self, context: OutputGeneratorContext) -> None:
        logging.info(f"Starting generation of {self._report_name} report")
        file_path = path.join(self.REPORTS_DIRECTORY, self._report_name)

        logging.info(f"Starting data processing of {self._report_name} report")
        data = self._generate_report_data(context)
        logging.info(f"Finished data processing of {self._report_name} report")

        with open(file_path, "w") as write:
            json.dump(data, write)
        logging.info(f"Finished generation of {self._report_name} report")
