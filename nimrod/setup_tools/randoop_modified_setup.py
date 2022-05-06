from nimrod.setup_tools.setup_tool import Setup_tool
from nimrod.tools.randoop_modified import Randoop_Modified
from nimrod.tools.safira import Safira


class Randoop_Modified_setup(Setup_tool):

    def generate_test_suite(self, scenario, project_dep):
        randoop = Randoop_Modified(
            java=project_dep.java,
            classpath=project_dep.parentReg,
            tests_src=project_dep.tests_dst + '/' + project_dep.project.get_project_name() + '/' + scenario.merge_scenario.get_merge_hash(),
            sut_class=project_dep.sut_class,
            sut_classes=project_dep.sut_classes,
            sut_method=project_dep.sut_method,
            params=self.tool_parameters
        )
        safira = Safira(java=project_dep.java, classes_dir=project_dep.parentReg, mutant_dir=project_dep.baseDir)
        try:
            self.test_suite = randoop.generate_with_impact_analysis(safira, True)
        except Exception as e:
            print(e)
            self.test_suite = randoop.generate_with_impact_analysis(safira, False)
        return self.test_suite
