import csv
import os

class Output_report():

    def __init__(self, output_path):
        self.path_output_csv = output_path
        self.path_output_csv_commit_pairs = output_path
        self.path_output_csv_test_conflicts = output_path

    def write_output_results(self, project_name, scenario, tool, which_parent, criteria_validation, class_information, method_information):
        if (os.path.isfile(os.getcwd().replace("/nimrod/proj","/")+'/semantic_study_result.csv') == False):
            self.create_result_file()
        else:
            self.path_output_csv = os.getcwd().replace("/nimrod/proj", "/") + "/semantic_study_result.csv"
        self.write_each_result(self.formate_output_line(project_name, scenario.merge_scenario.get_merge_hash(), tool, which_parent, "base-parent", criteria_validation, 0, class_information, method_information))
        self.write_each_result(self.formate_output_line(project_name, scenario.merge_scenario.get_merge_hash(), tool, which_parent, "parent-merge", criteria_validation, 1, class_information, method_information))
        self.write_each_result(self.formate_output_line(project_name, scenario.merge_scenario.get_merge_hash(), tool, which_parent, "base-merge", criteria_validation, 2, class_information, method_information))

    def write_output_results_test_conflicts(self, project_name, criteria_validation, class_information, method_information):
        if (os.path.isfile(os.getcwd().replace("/nimrod/proj","/")+'/test_conflicts.csv') == False):
            self.create_result_file_test_conflicts()
        else:
            self.path_output_csv_test_conflicts = os.getcwd().replace("/nimrod/proj", "/") + "/test_conflicts.csv"
        for one_commit_triplet in criteria_validation:
            self.write_each_result(self.path_output_csv_test_conflicts, self.formate_output_line_test_conflicts(project_name, one_commit_triplet, class_information, method_information))

    def write_output_results_commit_pairs(self, project_name, criteria_validation, class_information, method_information):
        if (os.path.isfile(os.getcwd().replace("/nimrod/proj","/")+'/behavior_changes_commit_pairs.csv') == False):
            self.create_result_file_commit_pairs()
        else:
            self.path_output_csv_commit_pairs = os.getcwd().replace("/nimrod/proj", "/") + "/behavior_changes_commit_pairs.csv"
        for one_commit_pair in criteria_validation:
            self.write_each_result(self.path_output_csv_commit_pairs, self.formate_output_line_commit_pairs(project_name, one_commit_pair, class_information, method_information))

    def create_result_file(self):
        with open(os.getcwd().replace("/nimrod/proj","/")+'/semantic_study_result.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["project_name", "merge_commit", "tool_under_analysis", "analyzed_parent", "commit_pair", "behavior_change", "failed_test_cases", "local_test_suite", "class_under-analysis", "method_under_analysis"])

        self.path_output_csv = os.getcwd().replace("/nimrod/proj","/")+"/semantic_study_result.csv"

    def create_result_file_commit_pairs(self):
        with open(os.getcwd().replace("/nimrod/proj","/")+'/behavior_changes_commit_pairs.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["project_name", "commitOneSha", "commitTwoSha", "tool", "behavior_change", "failed_test_cases", "local_test_suite", "class_under-analysis", "method_under_analysis"])

        self.path_output_csv_commit_pairs = os.getcwd().replace("/nimrod/proj","/")+"/behavior_changes_commit_pairs.csv"

    def create_result_file_test_conflicts(self):
        with open(os.getcwd().replace("/nimrod/proj","/")+'/test_conflicts.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["project_name", "base_commit", "parent_commit_test_suites", "other_parent_commit", "merge_commit", "tool", "behavior_change", "criteria", "failed_test_cases", "local_test_suite", "class_under-analysis", "method_under_analysis", "flaky_tests"])

        self.path_output_csv_test_conflicts = os.getcwd().replace("/nimrod/proj","/")+"/test_conflicts.csv"

    def write_each_result(self, file_path, output):
        with open(file_path, 'a+') as fd:
            writer = csv.writer(fd)
            writer.writerow(output)

    def formate_output_line(self, project_name, merge, tool, which_parent, commit_pair, criteria_validation, id_information, class_information, method_information):
        if (len(criteria_validation) > 0 and criteria_validation[id_information] != None):
            return [project_name, merge, tool, which_parent, commit_pair, criteria_validation[id_information][0], criteria_validation[id_information][1], criteria_validation[id_information][2], class_information, method_information]
        else:
            return [project_name, merge, tool,
                                  which_parent, commit_pair, "NO_INFORMATION", "", "","",""]

    def formate_output_line_commit_pairs(self, project_name, criteria_validation, class_information, method_information):
        if len(criteria_validation) > 1:
            return [project_name, criteria_validation[3], criteria_validation[4], criteria_validation[5], criteria_validation[0], criteria_validation[1], criteria_validation[2], class_information, method_information]
        else:
            return [project_name, "", "", "", "", "", "", class_information, method_information]

    def formate_output_line_test_conflicts(self, project_name, criteria_validation, class_information, method_information):
        try:
            if len(criteria_validation) > 1:
                return [project_name, criteria_validation[4], criteria_validation[5], criteria_validation[6], criteria_validation[7], criteria_validation[8], criteria_validation[0], criteria_validation[3], criteria_validation[1], criteria_validation[2], class_information, method_information, criteria_validation[9]]
        except Exception as e:
            print(e)
        return [project_name, "", "", "", "", "", "", "", class_information, method_information, ""]