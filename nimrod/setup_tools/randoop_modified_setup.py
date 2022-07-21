from nimrod.input_parsing.smat_input import SmatInput
from nimrod.setup_tools.setup_tool import Setup_tool
from nimrod.tools.randoop_modified import Randoop_Modified


class Randoop_Modified_setup(Setup_tool):

    def generate_test_suite(self, scenario, project_dep, input: SmatInput):
        randoop = Randoop_Modified(
            java=project_dep.java,
            classpath=project_dep.parentReg,
            tests_src=project_dep.tests_dst + '/' +
            project_dep.project.get_project_name() + '/' + input.scenario_commits.ancestor,
            sut_class=project_dep.sut_class,
            sut_classes=project_dep.sut_classes,
            sut_method=project_dep.sut_method,
            params=self.tool_parameters,
            scenario=scenario,
            input=input
        )
        self.test_suite = randoop.generate_with_impact_analysis()

        return self.test_suite
