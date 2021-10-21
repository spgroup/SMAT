import os
from nimrod.report.output import Output

class Output_semantic_conflicts(Output):

    def get_file_collumn_names(self):
        return ["project_name", "base_commit", "parent_commit_test_suites", "other_parent_commit", "merge_commit",
                "tool", "behavior_change", "criteria", "failed_test_cases", "local_test_suite", "class_under_analysis",
                "method_under_analysis", "flaky_tests", "jar_type"]

    def write_output_line(self, project_name, criteria_validation, class_information, method_information, jar_type):
        if (os.path.isfile(self.output_file_path) == False):
            self.create_result_file()
        for one_commit_triplet in criteria_validation:
            self.write_each_result(self.formate_output_line(project_name, one_commit_triplet, class_information, method_information, jar_type))

    def formate_output_line(self, project_name, criteria_validation, class_information, method_information, jar_type):
        try:
            if len(criteria_validation) > 1:
                return [project_name, criteria_validation[4], criteria_validation[5], criteria_validation[6],
                        criteria_validation[7], criteria_validation[8], criteria_validation[0], criteria_validation[3],
                        criteria_validation[1], criteria_validation[2], class_information, method_information, criteria_validation[9], jar_type]
        except Exception as e:
            print(e)
        return [project_name, "", "", "", "", "", "", "", "", "", class_information, method_information, "", jar_type]