import os
from typing import Dict, List
from nimrod.core.merge_scenario_under_analysis import MergeScenarioUnderAnalysis

from nimrod.test_suite_generation.generators.test_suite_generator import \
    TestSuiteGenerator
from nimrod.tests.utils import get_config
from nimrod.tools.java import Java
from nimrod.utils import generate_classpath


class RandoopTestSuiteGenerator(TestSuiteGenerator):
    SEARCH_BUDGET = int(get_config().get('test_suite_generation_search_budget', 300))

    TARGET_METHODS_LIST_FILENAME = 'methods_to_test.txt'
    TARGET_CLASS_LIST_FILENAME = 'classes_to_test.txt'

    def __init__(self, java: Java, randoop_jar: str, randoop_version: str) -> None:
        super().__init__(java)
        self._randoop_jar = randoop_jar
        self._randoop_version = randoop_version

    def get_generator_tool_name(self) -> str:
        return self._randoop_version

    def _execute_tool_for_tests_generation(self, input_jar: str, output_path: str, scenario: MergeScenarioUnderAnalysis, use_determinism: bool) -> None:
        params = [
            '-classpath', generate_classpath([input_jar, self._randoop_jar]),
            'randoop.main.Main',
            'gentests',
            '--junit-output-dir=' + output_path,
            f'--classlist={self._generate_target_classes_file(output_path, scenario.targets)}',
            f'--methodlist={self._generate_target_methods_file(output_path, scenario.targets)}'
        ]

        if use_determinism:
            params += ["--randomseed=10",
                       "--deterministic", "--time-limit=0", "--attempted-limit=4000"]
        else:
            params += [f"--time-limit={int(self.SEARCH_BUDGET)}"]

        self._java.exec_java(output_path, self._java.get_env(), 3000, *tuple(params))

    def _generate_target_classes_file(self, output_path: str, targets: "Dict[str, List[str]]"):
        filename = os.path.join(output_path, self.TARGET_CLASS_LIST_FILENAME)

        with open(filename, 'w') as f:
            fqcns = targets.keys()
            [f.write(fqcn.replace(" ", "") + "\n") for fqcn in fqcns]
            f.close()

        return filename

    def _generate_target_methods_file(self, output_path: str, targets: "Dict[str, List[str]]"):
        filename = os.path.join(output_path, self.TARGET_METHODS_LIST_FILENAME)

        with open(filename, 'w') as f:
            for fqcn, methods in targets.items():
                for method in methods:
                    method_signature = fqcn + "." + method
                    f.write(method_signature)

        return filename

    def _get_test_suite_class_paths(self, test_suite_path: str) -> List[str]:
        return [os.path.join(test_suite_path, "RegressionTest.java")]

    def _get_test_suite_class_names(self, test_suite_path: str) -> List[str]:
        return ["RegressionTest"]
