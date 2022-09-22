from nimrod.core.merge_scenario_under_analysis import MergeScenarioUnderAnalysis
from nimrod.setup_tools.setup_tool import Setup_tool
from nimrod.tests.utils import get_config
from nimrod.tools.bin import RANDOOP
from nimrod.test_suite_generation.generators.randoop_test_suite_generator import RandoopTestSuiteGenerator


class Randoop_setup(Setup_tool):

    def generate_test_suite(self, scenario, project_dep, input: MergeScenarioUnderAnalysis):
        use_determinism = bool(get_config().get('generate_deterministic_test_suites', False))
        randoop = RandoopTestSuiteGenerator(project_dep.java, RANDOOP, "RANDOOP")
        new_suite = randoop.generate_and_compile_test_suite(input, project_dep.parentReg, use_determinism)
        self.test_suite = self._convert_new_suite_to_old_test_suite(new_suite)
        return self.test_suite
