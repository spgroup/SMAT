from nimrod.input_parsing.smat_input import SmatInput
from nimrod.setup_tools.setup_tool import Setup_tool
from nimrod.test_suite_generation.generators.randoop_test_suite_generator import RandoopTestSuiteGenerator
from nimrod.tools.bin import MOD_RANDOOP


class Randoop_Modified_setup(Setup_tool):

    def generate_test_suite(self, scenario, project_dep, input: SmatInput):
        randoop = RandoopTestSuiteGenerator(project_dep.java, MOD_RANDOOP, "RANDOOP-MODIFIED")
        new_suite = randoop.generate_and_compile_test_suite(input, project_dep.parentReg)
        self.test_suite = self._convert_new_suite_to_old_test_suite(new_suite)
        return self.test_suite
