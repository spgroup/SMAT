from nimrod.input_parsing.smat_input import SmatInput
from nimrod.project_info.merge_scenario import MergeScenario
from nimrod.setup_tools.setup_tool import Setup_tool
from nimrod.test_suite_generation.generators.evosuite_test_suite_generator import EvosuiteTestSuiteGenerator


class Evosuite_setup(Setup_tool):
    def generate_test_suite(self, scenario: MergeScenario, project_dep, input: SmatInput = None):
        randoop = EvosuiteTestSuiteGenerator(project_dep.java)
        new_suite = randoop.generate_and_compile_test_suite(input, project_dep.parentReg)
        self.test_suite = self._convert_new_suite_to_old_test_suite(new_suite)
        return self.test_suite
