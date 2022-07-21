from nimrod.input_parsing.smat_input import SmatInput
from nimrod.project_info.merge_scenario import MergeScenario
from nimrod.setup_tools.setup_tool import Setup_tool
from nimrod.tools.evosuite import Evosuite


class Evosuite_setup(Setup_tool):
    def generate_test_suite(self, scenario: MergeScenario, project_dep, input: SmatInput = None):
        evosuite = Evosuite(
            java=project_dep.java,
            classpath=project_dep.parentReg,
            tests_src=project_dep.tests_dst + '/' + project_dep.project.get_project_name() +
            '/' + input.scenario_commits.ancestor,
            sut_class=project_dep.sut_class,
            sut_classes=project_dep.sut_classes,
            sut_method=project_dep.sut_method,
            scenario=scenario,
            params=self.tool_parameters,
            input=input
        )

        self.test_suite = evosuite.generate()

        return self.test_suite
