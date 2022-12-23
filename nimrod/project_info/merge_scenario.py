from nimrod.project_info.commit import Commit
import csv


class MergeScenario:

    def __init__(self, path_local_clone="", merge_information=""):
        self.path_local_clone = path_local_clone
        self.merge_scenario = Commit()

    def get_merge_scenarios(self):
        return self.merge_scenarios
