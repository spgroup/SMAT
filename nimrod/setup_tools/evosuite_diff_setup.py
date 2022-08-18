from nimrod.input_parsing.smat_input import SmatInput
from nimrod.setup_tools.setup_tool import Setup_tool
from nimrod.test_suite_generation.generators.evosuite_differential_test_suite_generator import EvosuiteDifferentialTestSuiteGenerator


class Evosuite_Diff_setup(Setup_tool):

    def generate_test_suite(self, scenario, project_dep, input: SmatInput = None):
        randoop = EvosuiteDifferentialTestSuiteGenerator(project_dep.java)
        new_suite = randoop.generate_and_compile_test_suite(input, project_dep.parentReg)
        self.test_suite = self._convert_new_suite_to_old_test_suite(new_suite)
        return self.test_suite