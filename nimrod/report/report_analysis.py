import os

from nimrod.report_metrics.target_method_metric import Target_Method_Metric
from nimrod.report_metrics.generated_object_metric import Generated_Object_Metric
from nimrod.report.report_writer import Report_Writer

class Report_Analysis:

    def __init__(self):
        self.target_method_metric = Target_Method_Metric()
        self.generated_object_metric = Generated_Object_Metric()
        self.report_writer = Report_Writer()

    def start_analysis(self, randoop_original, randoop_modified):
        self.checking_suites_and_reports(randoop_original[0][2], randoop_modified[0][2])
        right_path_index_original = len(randoop_original) - 1
        right_path_index_modified = len(randoop_modified) - 1
        self.checking_suites_and_reports(randoop_original[right_path_index_original][2], randoop_modified[right_path_index_modified][2])

    def checking_suites_and_reports(self, path_suite_original, path_suite_modified):
        if os.path.isdir(path_suite_original) and os.path.isdir(path_suite_modified):
            if self.all_reports(path_suite_original, path_suite_modified):
                self.suites_comparison(path_suite_original, path_suite_modified)
            else:
                print(
                    "It wasn't possible to compare the test suites because there are missing reports in paths: " + str(
                        path_suite_original) + " or " + str(path_suite_modified))
        else:
            print("It wasn't possible to make analysis because there are invalid path suites")

    def all_reports(self, path_suite_original, path_suite_modified):
        return os.path.isfile(path_suite_original + "/methods_report.csv") and os.path.isfile(path_suite_modified + "/methods_report.csv") \
               and os.path.isfile(path_suite_original + "/objects_report.csv") and os.path.isfile(path_suite_modified + "/objects_report.csv")

    def suites_comparison(self, path_suite_original, path_suite_modified):
        methods = self.target_method_metric.metrics_comparison(path_suite_original, path_suite_modified)
        objects = self.generated_object_metric.metrics_comparison(path_suite_original, path_suite_modified)

        if len(methods) == 0 or len(objects) == 0:
            print("It wasn't possible to compare the suites " + str(path_suite_original) + " and " + str(
                path_suite_modified))
        else:
            self.report_writer.write_methods_and_objects_report(path_suite_original, path_suite_modified, methods, objects)