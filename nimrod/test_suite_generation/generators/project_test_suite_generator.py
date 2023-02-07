import os
from typing import Dict, List
from nimrod.core.merge_scenario_under_analysis import MergeScenarioUnderAnalysis

from nimrod.test_suite_generation.generators.test_suite_generator import \
    TestSuiteGenerator
from nimrod.tools.java import Java
from nimrod.utils import generate_classpath
from nimrod.test_suite_generation.test_suite import TestSuite


class ProjectTestSuiteGenerator(TestSuiteGenerator):
    def get_generator_tool_name(self) -> str:
        return "PROJECT_TEST"
    
    def generate_and_compile_test_suite(self, scenario: MergeScenarioUnderAnalysis, input_jar: str, use_determinism: bool) -> TestSuite:
        merge_jar_test_path = scenario.scenario_jars.merge[:scenario.scenario_jars.merge.rfind("-")] + "-TestFiles.jar"
        project_test_suite_path = merge_jar_test_path[:merge_jar_test_path.rfind(os.sep)]

        return TestSuite(
            generator_name=self.get_generator_tool_name(),
            class_path=merge_jar_test_path,
            path=project_test_suite_path,
            test_classes_names=self._get_test_suite_class_names(merge_jar_test_path.replace(".jar", ".txt"))
        )

    def _get_test_suite_class_names(self, test_suite_path: str) -> List[str]:
        class_names = list()
        with open(test_suite_path, 'r') as f:
            class_names = f.readlines()
            class_names = [name.strip() for name in class_names]
        return class_names
    
    def _execute_tool_for_tests_generation(self, input_jar: str, output_path: str, scenario: MergeScenarioUnderAnalysis, use_determinism: bool) -> None:
        pass

    def _get_test_suite_class_paths(self, test_suite_path: str) -> List[str]:
        return []
