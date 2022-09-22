import json
from abc import ABC, abstractmethod
from os import makedirs, path
from typing import List, TypeVar, Generic

from nimrod.dynamic_analysis.semantic_conflict import SemanticConflict
from nimrod.input_parsing.smat_input import SmatInput
from nimrod.tests.utils import get_base_output_path

T = TypeVar("T")


class OutputGenerator(ABC, Generic[T]):
  REPORTS_DIRECTORY = path.join(get_base_output_path(), "reports")

  def __init__(self, report_name: str) -> None:
    super().__init__()
    makedirs(self.REPORTS_DIRECTORY, exist_ok=True)
    self._report_name = report_name + ".json"

  @abstractmethod
  def _generate_report_data(self, scenario: SmatInput, semantic_conflicts: List[SemanticConflict]) -> T:
    pass

  def write_report(self, scenario: SmatInput, semantic_conflicts: List[SemanticConflict]):
    file_path = path.join(self.REPORTS_DIRECTORY, self._report_name)
    data = self._generate_report_data(scenario, semantic_conflicts)

    with open(file_path, "w") as write:
        json.dump(data, write)
