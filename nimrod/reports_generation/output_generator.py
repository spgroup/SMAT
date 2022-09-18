from abc import ABC, abstractmethod
import json
from os import makedirs, path
from typing import TypeVar

from nimrod.tests.utils import get_base_output_path


class OutputGenerator(ABC):
  REPORTS_DIRECTORY = path.join(get_base_output_path(), "reports")

  def __init__(self, report_name: str) -> None:
    super().__init__()
    makedirs(self.REPORTS_DIRECTORY, exist_ok=True)
    self._report_name = report_name + ".json"

  @abstractmethod
  def _generate_report_data(self, context):
    pass

  def write_report(self, context):
    file_path = path.join(self.REPORTS_DIRECTORY, self._report_name)
    data = self._generate_report_data(context)

    with open(file_path, "w") as write:
        json.dump(data.__dict__, write)
