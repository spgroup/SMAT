import csv
import os
from collections import namedtuple

from nimrod.proj.project_dependencies import Project_dependecies
from nimrod.project_info.git_project import GitProject
from nimrod.project_info.merge_scenario import MergeScenario
from nimrod.report.output_behavior_change_commit_pair import Output_behavior_change_commit_pair
from nimrod.report.output_coverage_metric import Output_coverage_metric
from nimrod.report.output_report import Output_report
from nimrod.report.output_semantic_conflicts import Output_semantic_conflicts
from nimrod.report_metrics.coverage.coverage_report import Coverage_Report
from nimrod.report.report_analysis import Report_Analysis
from nimrod.setup_tools.evosuite_diff_setup import Evosuite_Diff_setup
from nimrod.setup_tools.evosuite_setup import Evosuite_setup
from nimrod.setup_tools.randoop_modified_setup import Randoop_Modified_setup
from nimrod.setup_tools.randoop_setup import Randoop_setup
from nimrod.setup_tools.tools import Tools
from nimrod.tests.utils import get_config

NimrodResult = namedtuple('NimrodResult', ['maybe_equivalent', 'not_equivalent',
                                           'coverage', 'differential',
                                           'timeout', 'test_tool', 'is_equal_coverage'])


class semantic_study:

    def __init__(self, path_local_project="", path_local_module_analysis="", project_name=""):
        config = get_config()
        self.project_dep = Project_dependecies(config, path_local_project, path_local_module_analysis, project_name)

        self.evosuite_setup = Evosuite_setup()
        self.evosuite_diff_setup = Evosuite_Diff_setup()
        self.randoop_setup = Randoop_setup()
        self.randoop_modified_setup = Randoop_Modified_setup()
        self.report_analysis = Report_Analysis()

        self.output_semantic_conflict = Output_semantic_conflicts(os.getcwd().replace("/nimrod/proj","/")+'/output-test-dest/' if os.getcwd().__contains__("/nimrod/proj") else os.getcwd() + "/output-test-dest/", "test_conflicts")
        self.output_coverage_metric = Output_coverage_metric(os.getcwd().replace("/nimrod/proj","/")+'/output-test-dest/' if os.getcwd().__contains__("/nimrod/proj") else os.getcwd() + "/output-test-dest/", "result_cobertura")

        self.output_report = Output_report(config["path_output_csv"])

    def set_git_project(self, path):
        self.project = GitProject(path)

    def get_commit_pairs(self, row):
        return [[row[11],row[10],row[3],row[5]], [row[12],row[10],row[4],row[5]], [row[11],row[13],row[3],row[2]], [row[12],row[13],row[4],row[2]]]

    def get_commit_triples(self, row):
        return [[row[10],row[11],row[13],row[5], row[3], row[2]], [row[10],row[12],row[13],row[5], row[4], row[2]]]

if __name__ == '__main__':

    config = get_config()
    with open(config['path_hash_csv']) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[1] == "true":
                print("Semantic Conflict Analysis")
                semantic_study_obj = semantic_study(project_name=row[0])
                coverage_report = Coverage_Report()
                merge = MergeScenario(merge_information=row)
                for i in range(0, 1):
                    evosuite = semantic_study_obj.evosuite_setup.run_tool_for_semantic_conflict_detection(semantic_study_obj, merge, row[10], row[11], row[12], row[13], row[5], row[3], row[4], row[2], Tools.EVOSUITE.value)
                    semantic_study_obj.output_semantic_conflict.write_output_line(row[0], evosuite, row[6], row[7])
                    evosuite_diff = semantic_study_obj.evosuite_diff_setup.run_tool_for_semantic_conflict_detection(semantic_study_obj, merge, row[10], row[11], row[12], row[13], row[5], row[3], row[4], row[2], Tools.DIFF_EVOSUITE.value)
                    semantic_study_obj.output_semantic_conflict.write_output_line(row[0], evosuite_diff, row[6], row[7])
                    randoop = semantic_study_obj.randoop_setup.run_tool_for_semantic_conflict_detection(semantic_study_obj, merge, row[10], row[11], row[12], row[13], row[5], row[3], row[4], row[2], Tools.RANDOOP.value)
                    semantic_study_obj.output_semantic_conflict.write_output_line(row[0], randoop, row[6], row[7])
                    randoop_modified = semantic_study_obj.randoop_modified_setup.run_tool_for_semantic_conflict_detection(semantic_study_obj, merge, row[10], row[11], row[12], row[13], row[5], row[3], row[4], row[2], Tools.RANDOOP_MOD.value)
                    semantic_study_obj.output_semantic_conflict.write_output_line(row[0], randoop_modified, row[6], row[7])
                    semantic_study_obj.report_analysis.start_analysis(randoop, randoop_modified)
                    coverage_report.generate_report(semantic_study_obj, merge, row[2], randoop, randoop_modified, row[0])