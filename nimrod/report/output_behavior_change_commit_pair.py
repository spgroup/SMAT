import os
from nimrod.report.output import Output

class Output_behavior_change_commit_pair(Output):

    def get_file_collumn_names(self):
        return ["project_name", "commitOneSha", "commitTwoSha", "tool", "behavior_change", "failed_test_cases",
                "local_test_suite", "class_under-analysis", "method_under_analysis"]

    def formate_output_line(self, project_name, criteria_validation, class_information, method_information):
        if len(criteria_validation) > 1:
            return [project_name, criteria_validation[4], criteria_validation[5], criteria_validation[8],
                    criteria_validation[0], criteria_validation[1], criteria_validation[2], class_information, method_information]
        else:
            return [project_name, "", "", "", "", "", "", class_information, method_information]

    def write_output_line(self, project_name, criteria_validation, class_information, method_information):
        if (os.path.isfile(self.output_file_path) == False):
            self.create_result_file()

        for one_commit_pair in criteria_validation:
            self.write_each_result(self.formate_output_line(project_name, one_commit_pair, class_information, method_information))
