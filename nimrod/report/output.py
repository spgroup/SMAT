from abc import ABC, abstractmethod
import csv
import os

class Output(ABC):
    output_file_path = ""
    output_file_name = ""

    def __init__(self, output_path, file_name):
        self.output_file_name = file_name
        self.output_file_path = self.create_result_file(output_path)

    def create_result_file(self, output_file_path):
        if (os.path.isfile(output_file_path+''+self.output_file_name+'.csv') == False):
            with open(output_file_path+''+self.output_file_name+'.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.get_file_collumn_names())

        return output_file_path+''+self.output_file_name+'.csv'

    def write_each_result(self, output):
        with open(self.output_file_path, 'a+') as fd:
            writer = csv.writer(fd)
            writer.writerow(output)

    @abstractmethod
    def get_file_collumn_names(self):
        pass

    @abstractmethod
    def write_output_line(self, project_name, criteria_validation, class_information, method_information):
        pass

    @abstractmethod
    def formate_output_line(self, project_name, criteria_validation, class_information, method_information):
        pass