from nimrod.report_metrics.metric import Metric

class Generated_Object_Metric(Metric):
    def metrics_comparison(self, path_suite_original, path_suite_modified) -> dict:
        objects_data = {}  # A dictionary the class of the object is the key and the value returned is a list with
        # the number of times that a objects from the class were created and how many of them are different from each
        # other, in that order, from randoop and randoop--

        objects_data = self.extract_data(objects_data, path_suite_original + "/objects_report.csv", True)
        objects_data = self.extract_data(objects_data, path_suite_modified + "/objects_report.csv", False)

        return objects_data

    def extract_data(self, data, report_path, randoop_original_report) -> dict:
        try:
            objects_report_file = open(report_path)
            objects_report = objects_report_file.read()
            objects_report_file.close()

            lines = objects_report.split("\n")
            for line in lines[1:-1]:  # Exclude the first one because contains the headers and the last one because it is a empty line
                cells = line.split(",")
                if randoop_original_report:
                    object_map = {cells[0]: [cells[1], 0, cells[2], 0, cells[3], 0, cells[4], 0]}
                    data.update(object_map)
                elif cells[0] in data:  # If the class is already in the dictionary, just change the value in the list
                    data.get(cells[0])[1] = cells[1]
                    data.get(cells[0])[3] = cells[2]
                    data.get(cells[0])[5] = cells[3]
                    data.get(cells[0])[7] = cells[4]
                else:
                    object_map = {cells[0]: [0, cells[1], 0, cells[2], 0, cells[3], 0, cells[4]]}
                    data.update(object_map)

            return data
        except:
            print("Error on objects_report.csv in " + str(report_path))
            return {}