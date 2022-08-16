import os
import re
import shutil
import fileinput
from nimrod.tools.java import Java
from nimrod.tools.maven import Maven
from nimrod.project_info.git_project import GitProject


class Project_dependecies:

    def __init__(self, config, path_local_project, path_local_module_analysis, project_name):
        self.config = config

        self.sut_class = None
        self.sut_classes = None
        self.sut_method = None
        self.dRegCp = None  # base
        self.classes_dir = None  # left
        self.mergeDir = None  # merge
        self.leftDir = None
        self.rightDir = None

        self.java = Java()
        self.maven = Maven(self.java, self.config['maven_home'])
        self.tests_dst = self.create_directory_test_destination()
        #self.tests_dst = self.config["tests_dst"]
        self.project = GitProject(path_local_project, path_local_module_analysis, project_name)
        self.projects_folder = self.config["projects_folder"]
        self.path_output_csv = self.config["path_output_csv"]

    def create_directory_test_destination(self):
        path_directory = os.getcwd().replace("/nimrod/proj","/")+'output-test-dest' if os.getcwd().__contains__("/nimrod/proj") else os.getcwd() + "/output-test-dest"
        if (os.path.isdir(path_directory) == False):
            os.mkdir(path_directory)
        return path_directory
