import os

class Report_Writer:

    def write_methods_and_objects_report(self, path_suite_original, path_suite_modified, methods, objects):
        suites_path = path_suite_original[:path_suite_original.rfind("/")]  # Get the directory where the test suites are
        reports_path = suites_path + "/reports"

        if os.path.isdir(reports_path) is False:
            os.mkdir(reports_path)

        suite_name_original = path_suite_original[path_suite_original.rfind("/") + 1:]
        suite_name_modified = path_suite_modified[path_suite_modified.rfind("/") + 1:]

        methods_report_name = reports_path + "/methods_report_" + suite_name_original + "_" + suite_name_modified + ".csv"
        methods_report_headers = "Methods called,Number of times(Original),Number of times(Modified),Modified - Original,Percentage(Gain/Loss),Number of times(Original-Normalized),Number of times(Modified-Normalized),Modified - Original,Percentage(Gain/Loss)\n"

        self.write_csv_file(methods_report_name, methods_report_headers, methods, False)

        objects_report_name = reports_path + "/objects_report_" + suite_name_original + "_" + suite_name_modified + ".csv"
        objects_report_headers = "Classes of objects created,Number of objects created(Original),Number of objects created(Modified),Modified - Original,Percentage(Gain/Loss),Number of unique objects manipulated(Original),Number of unique objects manipulated(Modified),Modified - Original,Percentage(Gain/Loss),Number of objects created(Original-Normalized),Number of objects created(Modified-Normalized),Modified - Original,Percentage(Gain/Loss),Number of unique objects manipulated(Original-Normalized),Number of unique objects manipulated(Modified-Normalized),Modified - Original,Percentage(Gain/Loss)\n"

        self.write_csv_file(objects_report_name, objects_report_headers, objects, True)

        print("The analysis of suites " + suite_name_original + " and " + suite_name_modified + " was done")

    def write_csv_file(self, path_csv, headers, data, is_object_report):
        with open(path_csv,"w") as output_file:
            output_file.write(headers)

            for key in data:
                text = key.replace(",","|") + "," + self.get_comparsion(int(data.get(key)[0]), int(data.get(key)[1]))

                if is_object_report:
                    text += "," + self.get_comparsion(int(data.get(key)[2]), int(data.get(key)[3])) + "," + self.get_comparsion(float(data.get(key)[4]), float(data.get(key)[5])) + "," + self.get_comparsion(float(data.get(key)[6]), float(data.get(key)[7])) + "\n"
                else:
                    text += "," + self.get_comparsion(float(data.get(key)[2]), float(data.get(key)[3])) + "\n"

                output_file.write(text)

            output_file.close()

    def get_comparsion(self, number_original, number_modified):
        sub = number_modified - number_original

        if number_original == 0:
            relative = "INF"
        elif number_modified == 0:
            relative = "-INF"
        else:
            relative = (sub / number_original) * 100
            relative = str(round(relative, 2))

        return str(number_original) + "," + str(number_modified) + "," + str(
            sub) + "," + "\"" + relative + "%\""