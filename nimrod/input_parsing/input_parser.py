import csv
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from nimrod.input_parsing.smat_input import ScenarioInformation, SmatInput

# This interface is responsible for parsing user input from a file into SMAT internal model.
# If you wish to implement a new parser, just create a new implementation of it.
class InputParser(ABC):
    @abstractmethod
    def parse_input(self, file_path: str) -> "List[SmatInput]":
        pass


class JsonInputParser(InputParser):
    def parse_input(self, file_path: str) -> "List[SmatInput]":
        json_data: List[Dict[str, Any]] = []
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)

        return [self._convert_to_internal_representation(scenario) for scenario in json_data]

    def _convert_to_internal_representation(self, scenario: "Dict[str, Any]"):
        scenario_commits_json: Any = scenario.get('scenarioCommits')
        scenario_jars_json: Any = scenario.get('scenarioJars')

        return SmatInput(
            project_name=str(scenario.get('projectName')),
            run_analysis=bool(scenario.get('runAnalysis')),
            scenario_commits=ScenarioInformation(
                base=scenario_commits_json.get('base'),
                left=scenario_commits_json.get('left'),
                right=scenario_commits_json.get('right'),
                merge=scenario_commits_json.get('merge'),
            ),
            targets=scenario.get('targets', dict()),
            scenario_jars=ScenarioInformation(
                base=scenario_jars_json.get('base'),
                left=scenario_jars_json.get('left'),
                right=scenario_jars_json.get('right'),
                merge=scenario_jars_json.get('merge'),
            ),
            jar_type=str(scenario.get('jarType'))
        )


class CsvInputParser(InputParser):
    def parse_input(self, file_path: str) -> "List[SmatInput]":
        with open(file_path, 'r') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            return [self._convert_to_internal_representation(scenario) for scenario in csv_data]

    def _convert_to_internal_representation(self, row: "List[str]"):
        return SmatInput(
            project_name=row[0],
            run_analysis=row[1] == "true",
            scenario_commits=ScenarioInformation(
                base=row[2],
                left=row[3],
                right=row[4],
                merge=row[5],
            ),
            targets=self._build_targets_from_old_entry(row[6], row[7]),
            scenario_jars=ScenarioInformation(
                base=row[10],
                left=row[11],
                right=row[12],
                merge=row[13],
            ),
            jar_type=row[14]
        )

    def _build_targets_from_old_entry(self, class_list: str, method_list: str):
        classes = class_list.split(' | ')
        targets: Dict[str, List[str]] = dict()
        for class_name in classes:
            targets[class_name] = []

        targets[classes[0]] = [method_list.replace('|', ",")]

        return targets
