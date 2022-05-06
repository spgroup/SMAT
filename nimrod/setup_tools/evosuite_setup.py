from nimrod.setup_tools.setup_tool import Setup_tool
from nimrod.tools.evosuite import Evosuite
from nimrod.tools.safira import Safira


class Evosuite_setup(Setup_tool):

    def generate_test_suite(self, scenario, project_dep):
        evosuite = Evosuite(
            java=project_dep.java,
            classpath=project_dep.parentReg,
            tests_src=project_dep.tests_dst + '/' + project_dep.project.get_project_name() + '/' + scenario.merge_scenario.get_merge_hash(),
            sut_class=project_dep.sut_class,
            sut_classes=project_dep.sut_classes,
            sut_method=project_dep.sut_method,
            params=self.tool_parameters
        )
        safira = Safira(java=project_dep.java, classes_dir=project_dep.parentReg,
                        mutant_dir=project_dep.baseDir)
        self.test_suite = evosuite.generate_with_impact_analysis(safira, False)

        return self.test_suite