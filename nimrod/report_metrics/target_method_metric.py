import re
from nimrod.report_metrics.metric import Metric

class Target_Method_Metric(Metric):
    def metrics_comparison(self, path_suite_original, path_suite_modified) -> dict:
        methods_data = {}  # A dictionary in which the method name is the key and the value returned is a list with
        # the number of times that the method was called for original randoop and randoop--

        methods_data = self.extract_data(methods_data, path_suite_original + "/methods_report.csv", True)
        methods_data = self.extract_data(methods_data, path_suite_modified + "/methods_report.csv", False)

        return methods_data
    
    def extract_data(self, data, report_path, randoop_original_report) -> dict:
        try:
            methods_report_file = open(report_path)
            methods_report = methods_report_file.read()
            methods_report_file.close()

            lines = methods_report.split("\n")
            for line in lines[1:-1]:  # Exclude the first one because contains the headers and the last one because it is a empty line
                cells = re.split("(?<=\"),", line)
                aux = re.split(",", cells[1])
                cells[1] = aux[0]
                cells[2] = aux[1]
                if randoop_original_report:
                    method_map = {cells[0]: [cells[1], 0, cells[2], 0]}
                    data.update(method_map)
                elif cells[0] in data:  # If the method signature is already in the dictionary, just change the value in the list
                    data.get(cells[0])[1] = cells[1]
                    data.get(cells[0])[3] = cells[2]
                else:
                    method_map = {cells[0]: [0, cells[1], 0, cells[2]]}
                    data.update(method_map)
        except:
            print("Error on methods_report.csv in " + str(report_path))

        return data