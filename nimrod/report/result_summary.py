import os
from nimrod.report.output import Output

class Result_Summary(Output):

    def __init__(self, output_path, file_name):
        Output.__init__(self, output_path, file_name)
        self.summary = []
        self.randoop_suites = {}
        self.randoop_mod_suites = {}

    def generate_summary(self, test_conflict_report_file, coverage_report_file):
        test_conflict_report = open(test_conflict_report_file)
        test_conflicts = test_conflict_report.read()
        test_conflict_report.close()

        lines = test_conflicts.split("\n")
        current_merge_scenario = ""
        current_target_method = ""
        parent_one = ""
        parent_two = ""
        merge_scenario_values = []

        for line in lines[1:-1]:
            values = line.split(",");
            if(current_merge_scenario == ""):
                current_merge_scenario = values[4]
                current_target_method = values[11]
            if (parent_one == ""):
                parent_one = values[2]
            if (parent_two == "" and values[3] != parent_one and values[3] != "NOT-REQUIRED"):
                parent_two = values[3]

            if ((values[4] == current_merge_scenario or values[4] == "NOT-REQUIRED") and values[11] == current_target_method):
                merge_scenario_values.append(values)
            else:
                self.summary_by_target_method(merge_scenario_values, parent_one, parent_two, "transformed")
                self.summary_by_target_method(merge_scenario_values, parent_one, parent_two, "original")
                self.summary_by_target_method(merge_scenario_values, parent_one, parent_two, "serialized")

                current_merge_scenario = values[4]
                current_target_method = values[11]
                merge_scenario_values = []
                merge_scenario_values.append(values)
                parent_one = ""
                parent_two = ""

        if(len(merge_scenario_values)>0):
            self.summary_by_target_method(merge_scenario_values, parent_one, parent_two, "transformed")
            self.summary_by_target_method(merge_scenario_values, parent_one, parent_two, "original")
            self.summary_by_target_method(merge_scenario_values, parent_one, parent_two, "serialized")

        for summary_line in self.summary:
            if (summary_line[3]+"-"+summary_line[4] in self.randoop_suites and summary_line[3]+"-"+summary_line[4] in self.randoop_mod_suites):
                suite_original = self.randoop_suites[summary_line[3]+"-"+summary_line[4]][0]
                suite_modified = self.randoop_mod_suites[summary_line[3]+"-"+summary_line[4]][0]
                comparison = self.get_value_metric_object_creation(suite_original, suite_modified, str(summary_line[3]).split(" | ")[0].replace("$","."),
                                                                   str(summary_line[1]).split("(")[0], summary_line[2])

                coverage_report = open(coverage_report_file)
                coverage_report_info = coverage_report.read()
                coverage_report.close()

                lines = coverage_report_info.split("\n")

                for line in lines[1:-1]:
                    values = line.split(",");
                    if (suite_original == values[3] and suite_modified == values[4] and summary_line[3] == values[0] and summary_line[4] == values[1]):
                        try:
                            line_coverage_original = 0
                            line_coverage_modified = 0
                            if (values[15] != ""):
                                line_coverage_modified = float(values[15])
                            if (values[14] != ""):
                                line_coverage_original = float(values[14])

                            method_coverage_original = 0
                            method_coverage_modified = 0
                            if (values[18] != ""):
                                method_coverage_modified = float(values[18])
                            if (values[17] != ""):
                                method_coverage_original = float(values[17])

                            if (line_coverage_modified > line_coverage_original):
                                summary_line[14] = True
                            elif (line_coverage_modified == line_coverage_original):
                                summary_line[14] = "SAME"
                            else:
                                summary_line[14] = False

                            if (method_coverage_modified > method_coverage_original):
                                summary_line[15] = True
                            elif (method_coverage_modified == method_coverage_original):
                                summary_line[15] = "SAME"
                            else:
                                summary_line[15] = False

                        except Exception:
                            print("It was not possible to get coverage information. \n")

                self.randoop_suites[summary_line[3]+"-"+summary_line[4]].remove(suite_original)
                self.randoop_mod_suites[summary_line[3]+"-"+summary_line[4]].remove(suite_modified)
                summary_line[12] = comparison[0]
                summary_line[13] = comparison[1]

        for summary_line in self.summary:
            self.write_output_line(summary_line)

    def get_value_metric_object_creation(self, path_original, path_modified, merge_scenario, target_class, target_method):
        target_class = target_class.split(" | ")[0]
        target_method = target_method.split("(")[0]
        target_method_comparison = ""
        target_class_comparison = ""
        if (path_original.split(merge_scenario)[0]+merge_scenario+"/reports" == path_modified.split(merge_scenario)[0]+merge_scenario+"/reports"):
            if (os.path.exists(path_original.split(merge_scenario)[0]+merge_scenario+"/reports/methods_report_"+str(path_original.split("/")[-1])+"_"+str(path_modified.split("/")[-1])+".csv")):
                report_original_modified_randoop_file = open(path_original.split(merge_scenario)[0]+merge_scenario+"/reports/methods_report_"+str(path_original.split("/")[-1])+"_"+str(path_modified.split("/")[-1])+".csv")
                report_original_modified_randoop = report_original_modified_randoop_file.read()
                report_original_modified_randoop_file.close()
                lines = report_original_modified_randoop.split("\n")

                for line in lines[1:]:
                    values = line.split(",");
                    if (target_class+"."+target_method in values[0]):
                        if (values[8] != ""):
                            target_method_comparison = values[8].replace("\"","")
                        else:
                            target_method_comparison = 0
                        break
                if (target_method_comparison == ""):
                    target_method_comparison = "UNAVAILABLE-INFORMATION"

        if (os.path.exists(path_original.split(merge_scenario)[0]+merge_scenario+"/reports/objects_report_"+str(path_original.split("/")[-1])+"_"+str(path_modified.split("/")[-1])+".csv")):
            report_original_modified_randoop_file = open(path_original.split(merge_scenario)[0]+merge_scenario+"/reports/objects_report_"+str(path_original.split("/")[-1])+"_"+str(path_modified.split("/")[-1])+".csv")
            report_original_modified_randoop = report_original_modified_randoop_file.read()
            report_original_modified_randoop_file.close()
            lines = report_original_modified_randoop.split("\n")

            for line in lines[1:]:
                values = line.split(",");
                if ("class "+str(target_class) == values[0]):
                    if (values[16] != ""):
                        target_class_comparison = values[16].replace("\"","")
                    else:
                        target_class_comparison = 0
                    break
            if (target_class_comparison == ""):
                target_class_comparison = "UNAVAILABLE INFORMATION"

        return [target_class_comparison, target_method_comparison]

    def get_file_collumn_names(self):
        return ["project_name","merge_scenario","target_class","target_method","target_parent","jar_type","conflict_detection_first_criterion","tools",
                "conflict_detection_first_criterion","tools","behavior_change","tools","improvement_object_creation",
                "improvement_on_target_method_call","improvement_on_coverage_target_class","improvement_on_coverage_target_method"]

    def write_output_line(self, text):
        if (os.path.isfile(self.output_file_path) == False):
            self.create_result_file()
        self.write_each_result(text)

    def formate_output_line(self, project_name, criteria_validation, class_information, method_information):
        pass

    def summary_by_target_method(self, values, parent_one, parent_two, jar_type):
        self.summary_by_target_commit(values, parent_one, jar_type)
        self.summary_by_target_commit(values, parent_two, jar_type)

    def summary_by_target_commit(self, values, target_parent, jar_type):
        conflict_occurrence_first = False
        conflict_tools_first = []
        conflict_occurrence_second = False
        conflict_tools_second = []
        behavior_change = False
        behavior_change_tools = []
        project_name = ""
        merge_commit = ""
        target_class = ""
        target_method = ""

        for value in values:
            if (value[13] == jar_type and value[2] == target_parent):
                if (value[6] == 'True'):
                    if (value[7] == "FIRST_CRITERION"):
                        conflict_occurrence_first = True;
                        if (not value[5] in conflict_tools_first):
                            conflict_tools_first.append(value[5])
                    elif (value[7] == "SECOND_CRITERION"):
                        conflict_occurrence_second = True;
                    if (not value[5] in conflict_tools_second):
                        conflict_tools_second.append(value[5])
                    elif (value[7] == "BEHAVIOR-CHANGE-COMMIT-PAIR"):
                        behavior_change = True;
                    if (not value[5] in behavior_change_tools):
                        behavior_change_tools.append(value[5])

                if (project_name == ""):
                    project_name = value[0]
                if (merge_commit == ""):
                    merge_commit = value[4]
                if (target_class == ""):
                    target_class = value[10].replace("\"","")
                if (target_method == ""):
                    target_method = value[11].replace("\"","")

                if(value[5] == "RANDOOP" and not value[4] == "NOT-REQUIRED"):
                    if (not value[4]+"-"+value[2] in self.randoop_suites):
                        self.randoop_suites[value[4]+"-"+value[2]] = [value[9]]
                    elif (not value[9] in self.randoop_suites[value[4]+"-"+value[2]] ):
                        aux = self.randoop_suites[value[4]+"-"+value[2]]
                        aux.append(value[9])
                        self.randoop_suites[value[4]+"-"+value[2]] = aux
                if(value[5] == "RANDOOP-MODIFIED" and not value[4] == "NOT-REQUIRED"):
                    if (not value[4]+"-"+value[2] in self.randoop_mod_suites):
                        self.randoop_mod_suites[value[4]+"-"+value[2]] = [value[9]]
                    elif (not value[9] in self.randoop_mod_suites[value[4]+"-"+value[2]] ):
                        aux = self.randoop_mod_suites[value[4]+"-"+value[2]]
                        aux.append(value[9])
                        self.randoop_mod_suites[value[4]+"-"+value[2]] = aux

        if (project_name != ""):
            self.summary.append([project_name, target_class, target_method, merge_commit, target_parent, jar_type, str(conflict_occurrence_first),
                                 str(conflict_tools_first).replace("\'",""), str(conflict_occurrence_second), str(conflict_tools_second).replace("\'",""),
                                 str(behavior_change),str(behavior_change_tools).replace("\'",""),"","","",""])
