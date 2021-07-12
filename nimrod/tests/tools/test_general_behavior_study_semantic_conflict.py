import os
import shutil
from unittest import TestCase

from nimrod.proj.semantic_study import semantic_study
from nimrod.project_info.merge_scenario import MergeScenario
from nimrod.setup_tools.tools import Tools


class TestGeneralBehaviorSemanticStudy(TestCase):

    def test_generate(self):
        semantic_study_obj = semantic_study()
        row = self.get_input_as_row()

        merge = MergeScenario(merge_information=row)

        evosuite = semantic_study_obj.evosuite_diff_setup.run_tool_for_semantic_conflict_detection(semantic_study_obj, merge, row[10], row[11], row[12], row[13], row[5], row[3], row[4], row[2], Tools.DIFF_EVOSUITE.value)

        # evosuite[0-1,4-5][0] -> result for semantic conflict detected by one of the criteria
        if (evosuite[0][0] == True or evosuite[1][0] == True or evosuite[4][0] == True or evosuite[5][0] == True):
            isConflictDetected = True
            self.assertTrue(isConflictDetected)

        # evosuite[2-3,6-7][0] -> result for behavior change detected by one of the criteria
        if (evosuite[2][0] == True or evosuite[3][0] == True or evosuite[6][0] == True or evosuite[7][0] == True):
            isBehaviorChangeDetected = True
            self.assertTrue(isBehaviorChangeDetected)

        directory = str(semantic_study_obj.output_semantic_conflict.output_file_path).split("test_conflicts.csv")[0]
        os.path.isdir(directory+"/4d9ba9d221d879507440feb084fa7521b95111ec/evosuite_1")
        self.assertTrue(os.path.isdir(directory+"/4d9ba9d221d879507440feb084fa7521b95111ec/evosuite_1"))
        self.assertTrue(os.path.isdir(directory+"/4d9ba9d221d879507440feb084fa7521b95111ec/evosuite_2"))

        self.remove_generated_suites(directory)

    def test_generate_coverage_metric_report(self):
        semantic_study_obj = semantic_study()

        row = self.get_input_as_row()
        merge = MergeScenario(merge_information=row)

        randoop = semantic_study_obj.randoop_setup.run_tool_for_semantic_conflict_detection(semantic_study_obj, merge, row[10], row[11], row[12], row[13], row[5], row[3], row[4], row[2], Tools.RANDOOP)
        randoop_modified = semantic_study_obj.randoop_modified_setup.run_tool_for_semantic_conflict_detection(semantic_study_obj, merge, row[10], row[11], row[12], row[13], row[5], row[3], row[4], row[2], Tools.RANDOOP_MOD)
        semantic_study_obj.report_analysis.start_analysis(randoop, randoop_modified)

        directory = str(semantic_study_obj.output_semantic_conflict.output_file_path).split("test_conflicts.csv")[0]
        self.assertTrue(os.path.isfile(directory+"/4d9ba9d221d879507440feb084fa7521b95111ec/reports/methods_report_randoop_1_randoop-modified_1.csv"))
        self.assertTrue(os.path.isfile(directory+"/4d9ba9d221d879507440feb084fa7521b95111ec/reports/methods_report_randoop_2_randoop-modified_2.csv"))
        self.assertTrue(os.path.isfile(directory+"/4d9ba9d221d879507440feb084fa7521b95111ec/reports/objects_report_randoop_1_randoop-modified_1.csv"))
        self.assertTrue(os.path.isfile(directory+"/4d9ba9d221d879507440feb084fa7521b95111ec/reports/objects_report_randoop_2_randoop-modified_2.csv"))

        self.remove_generated_suites(directory)

    def remove_generated_suites(self, directory):
        try:
            shutil.rmtree(directory)
            print("Directory '% s' has been removed successfully" % directory)
        except OSError as error:
            print(error)
            print("Directory '% s' can not be removed" % directory)

    def get_input_as_row(self):
        jar_path = self.get_input_jar_directory();

        return ["fitnesse","false","4d9ba9d221d879507440feb084fa7521b95111ec","d24741cd3","6c383370e",
               "87a4b54f94f7dbe48bdfde0dae874e36d48f43df", "fitnesse.testsystems.slim.tables.SlimTableFactory",
               "SlimTableFactory()","","",
               jar_path+"base.jar:",
               jar_path+"left.jar:",
               jar_path+"right.jar:",
               jar_path+"merge.jar:",
               "false","false","false"]

    def get_input_jar_directory(self):
        if(os.getcwd().__contains__("tools")):
            return os.getcwd().replace("nimrod/tests/tools", "nimrod/tests/example/semantic_conflict/transformed/")
        else:
            return os.getcwd()+"/nimrod/tests/example/semantic_conflict/transformed/"