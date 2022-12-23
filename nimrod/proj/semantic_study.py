import logging
import os
from collections import namedtuple

from nimrod.input_parsing.input_parser import CsvInputParser, JsonInputParser
from nimrod.core.merge_scenario_under_analysis import MergeScenarioUnderAnalysis
from nimrod.proj.project_dependencies import Project_dependecies
from nimrod.project_info.git_project import GitProject
from nimrod.project_info.merge_scenario import MergeScenario
from nimrod.report.output_behavior_change_commit_pair import \
    Output_behavior_change_commit_pair
from nimrod.report.output_coverage_metric import Output_coverage_metric
from nimrod.report.output_report import Output_report
from nimrod.report.output_semantic_conflicts import Output_semantic_conflicts
from nimrod.report.report_analysis import Report_Analysis
from nimrod.report.result_summary import Result_Summary
from nimrod.report_metrics.coverage.coverage_report import Coverage_Report
from nimrod.setup_tools.evosuite_diff_setup import Evosuite_Diff_setup
from nimrod.setup_tools.evosuite_setup import Evosuite_setup
from nimrod.setup_tools.randoop_modified_setup import Randoop_Modified_setup
from nimrod.setup_tools.randoop_setup import Randoop_setup
from nimrod.setup_tools.tools import Tools
from nimrod.tests.utils import get_config, setup_logging

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

        self.output_semantic_conflict = Output_semantic_conflicts(os.getcwd().replace(
            "/nimrod/proj", "/")+'/output-test-dest/' if os.getcwd().__contains__("/nimrod/proj") else os.getcwd() + "/output-test-dest/", "test_conflicts")
        self.output_coverage_metric = Output_coverage_metric(os.getcwd().replace(
            "/nimrod/proj", "/")+'/output-test-dest/' if os.getcwd().__contains__("/nimrod/proj") else os.getcwd() + "/output-test-dest/", "result_cobertura")

        self.output_report = Output_report(config["path_output_csv"])
        self.results_summary = Result_Summary(os.getcwd().replace("/nimrod/proj", "/")+'/output-test-dest/' if os.getcwd(
        ).__contains__("/nimrod/proj") else os.getcwd() + "/output-test-dest/", "results_summary")


if __name__ == '__main__':
    config = get_config()
    setup_logging()

    parsed_input: "list[MergeScenarioUnderAnalysis]" = None
    if config.get('input_path'):
        parsed_input = JsonInputParser().parse_input(config.get('input_path'))
    elif config.get('path_hash_csv'):
        logging.WARN(
            'DEPRECATED: Providing input data with `path_hash_csv` is deprecated and will be removed in future versions of SMAT. Use `input_path` instead.')
        parsed_input = CsvInputParser().parse_input(config.get('path_hash_csv'))
    else:
        logging.FATAL('Non input file provided')
        exit(1)

    scenarios = [
        scenario for scenario in parsed_input if scenario.run_analysis]
    for scenario in scenarios:
        logging.info(
            "Starting Semantic Conflict Analysis for project %s", scenario.project_name)

        semantic_study_obj = semantic_study(project_name=scenario.project_name)
        local_file_result = semantic_study_obj.output_semantic_conflict.output_file_path
        local_file_coverage = semantic_study_obj.output_coverage_metric.output_file_path
        coverage_report = Coverage_Report()
        merge = MergeScenario()

        evosuite = semantic_study_obj.evosuite_setup.run_tool_for_semantic_conflict_detection(
            semantic_study_obj, merge, Tools.EVOSUITE.value, scenario)
        semantic_study_obj.output_semantic_conflict.write_output_line(
            scenario.project_name, evosuite, (' | ').join(scenario.targets.keys()), '', scenario.jar_type)
        evosuite_diff = semantic_study_obj.evosuite_diff_setup.run_tool_for_semantic_conflict_detection(
            semantic_study_obj, merge, Tools.DIFF_EVOSUITE.value, scenario)
        semantic_study_obj.output_semantic_conflict.write_output_line(
            scenario.project_name, evosuite_diff, (' | ').join(scenario.targets.keys()), '', scenario.jar_type)
        randoop = semantic_study_obj.randoop_setup.run_tool_for_semantic_conflict_detection(
            semantic_study_obj, merge, Tools.RANDOOP.value, scenario)
        semantic_study_obj.output_semantic_conflict.write_output_line(
            scenario.project_name, randoop, (' | ').join(scenario.targets.keys()), '', scenario.jar_type)
        randoop_modified = semantic_study_obj.randoop_modified_setup.run_tool_for_semantic_conflict_detection(
            semantic_study_obj, merge, Tools.RANDOOP_MOD.value, scenario)
        semantic_study_obj.output_semantic_conflict.write_output_line(
            scenario.project_name, randoop_modified, (' | ').join(scenario.targets.keys()), '', scenario.jar_type)
        semantic_study_obj.report_analysis.start_analysis(
            randoop, randoop_modified)
        coverage_report.generate_report(semantic_study_obj, merge, scenario.scenario_commits.base,
                                        randoop, randoop_modified, scenario.project_name, scenario.jar_type, scenario)

        semantic_study_obj = semantic_study()
        semantic_study_obj.results_summary.generate_summary(
            semantic_study_obj.output_semantic_conflict.output_file_path, semantic_study_obj.output_coverage_metric.output_file_path)
