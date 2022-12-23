from abc import ABC, abstractmethod
import logging
import os
from nimrod.core.merge_scenario_under_analysis import MergeScenarioUnderAnalysis
from nimrod.project_info.merge_scenario import MergeScenario

from nimrod.setup_tools.behaviour_check import Behaviour_check
from nimrod.test_suite_generation.test_suite import TestSuite
from nimrod.tools.junit import JUnit

from nimrod.tools.suite_generator import Suite


class Setup_tool(ABC):

    def __init__(self):
        self.test_suite = None
        self.tool_parameters = None
        self.behaviour_change = Behaviour_check()

    def setup_for_partial_merge_scenario(self, evo, scenario, jarBase, jarParent=None, jarMerge=None):
        try:
            evo.project_dep.baseDir = jarBase
            evo.project_dep.parentReg = jarParent
            evo.project_dep.mergeDir = jarMerge
            evo.project_dep.sut_classes = scenario.merge_scenario.get_sut_classes()
            evo.project_dep.sut_class = scenario.merge_scenario.get_sut_class()
            evo.project_dep.sut_method = scenario.merge_scenario.get_sut_method()
        except:
            print("Some project versions could not be evaluated")

    def setup_for_full_merge_scenario(self, evo, scenario, jarBase, jarParentForGeneration, jarOtherParent, jarMerge):
        try:
            self.setup_for_partial_merge_scenario(evo, scenario, jarBase, jarParentForGeneration, jarMerge)
            evo.project_dep.parentNotReg = jarOtherParent
        except:
            print("Some project versions could not be evaluated")

    def run_tool_for_semantic_conflict_detection(self, evo, scenario: MergeScenario, tool: str, input: MergeScenarioUnderAnalysis):
        conflict_info = []

        jarBase = input.scenario_jars.base
        jarParentLeft = input.scenario_jars.left
        jarParentRight = input.scenario_jars.right
        jarMerge = input.scenario_jars.merge

        commitBaseSha = input.scenario_commits.base
        commitParentLeft = input.scenario_commits.left
        commitParentRight = input.scenario_commits.right
        commitMergeSha = input.scenario_commits.merge

        try:
            self.setup_for_full_merge_scenario(evo, scenario, jarBase, jarParentLeft, jarParentRight, jarMerge)
            test_results_left = self.generate_and_run_test_suites(evo, scenario, commitBaseSha, commitParentLeft,
                                    commitParentRight, commitMergeSha, conflict_info, tool, input=input)
            if (len(test_results_left[0]) > 0):
                self.check_semantic_conflict_occurrence(test_results_left[0], test_results_left[1], test_results_left[2],
                                    test_results_left[3], test_results_left[4], commitBaseSha, commitParentLeft,
                                    commitParentRight, commitMergeSha, tool, conflict_info)
                self.check_behavior_change_commit_pair(test_results_left[0], test_results_left[1], test_results_left[2],
                                    test_results_left[4], commitBaseSha, commitParentLeft, commitMergeSha, tool, conflict_info)

            self.setup_for_full_merge_scenario(evo, scenario, jarBase, jarParentRight, jarParentLeft, jarMerge)
            test_results_right = self.generate_and_run_test_suites(evo, scenario, commitBaseSha, commitParentRight,
                                    commitParentLeft, commitMergeSha, conflict_info, tool, input=input)
            if (len(test_results_right[0]) > 0):
                self.check_semantic_conflict_occurrence(test_results_right[0], test_results_right[1], test_results_right[2],
                                    test_results_right[3], test_results_right[4], commitBaseSha, commitParentRight,
                                    commitParentLeft, commitMergeSha, tool, conflict_info)
                self.check_behavior_change_commit_pair(test_results_right[0], test_results_right[1], test_results_right[2],
                                    test_results_right[4], commitBaseSha, commitParentRight, commitMergeSha, tool, conflict_info)

        except Exception as e:
            logging.error(e)
            print("Some project versions could not be evaluated")

        return conflict_info

    def run_tool_for_behaviour_change_detection(self, evo, scenario, jarCommitOne, jarCommitTwo, commitOne, commitTwo, tool, input: MergeScenarioUnderAnalysis = None):
        conflict_info = []
        try:
            self.setup_for_partial_merge_scenario(evo, scenario, jarCommitOne, jarCommitTwo)
            test_results_left = self.generate_and_run_test_suites_for_commit_pair(evo, scenario, commitOne, commitTwo,
                                conflict_info, tool, input)
            if (len(test_results_left[0]) > 0):
                conflict_info.append(self.behaviour_change.check_different_test_results_for_commit_pair(test_results_left[1],
                                test_results_left[2], test_results_left[0], commitOne, commitTwo, tool))
        except:
            print("Some project versions could not be evaluated")

        return conflict_info

    def generate_and_run_test_suites(self, evo, scenario: MergeScenario, commitBaseSha, commitParentTestSuite, commitOtherParent,
                                     commitMergeSha, conflict_info, tool, input: MergeScenarioUnderAnalysis = None):
        path_suite = []
        test_result_base = set()
        test_result_parent_test_suite = set()
        test_result_other_parent = set()
        test_result_merge = set()
        try:
            logging.info("Starting test suite generation with %s tool", tool)
            path_suite = self.generate_test_suite(scenario, evo.project_dep, input)
            logging.info("Finished test suite generation with %s tool", tool)

            logging.info("Starting test suite execution for commit %s",
                         input.scenario_commits.base)
            test_result_base = self.run_test_suite(evo.project_dep.parentReg, input.targets,
                                                   evo.project_dep.baseDir, evo.project_dep)
            test_result_parent_test_suite = self.run_test_suite(evo.project_dep.parentReg, input.targets,
                                                                evo.project_dep.parentReg, evo.project_dep)
            test_result_other_parent = self.run_test_suite(evo.project_dep.parentReg, input.targets,
                                                           evo.project_dep.parentNotReg, evo.project_dep)
            test_result_merge = self.run_test_suite(evo.project_dep.parentReg, input.targets,
                                                    evo.project_dep.mergeDir, evo.project_dep)
        except Exception as exception:
            print(exception)
            print("Some project versions could not be evaluated")
            conflict_info.append(["NONE", set(), "NO-INFORMATION", commitBaseSha, commitParentTestSuite, commitMergeSha,
                                    tool])

        return path_suite, test_result_base, test_result_parent_test_suite, test_result_other_parent, test_result_merge

    def generate_and_run_test_suites_for_commit_pair(self, evo, scenario: MergeScenario, commitOne, commitTestSuite, conflict_info, tool, input: MergeScenarioUnderAnalysis = None):
        path_suite = []
        test_result_base = set()
        test_result_parent_test_suite = set()

        try:
            path_suite = self.generate_test_suite(scenario, evo.project_dep)

            test_result_base = self.run_test_suite(evo.project_dep.parentReg, input.targets,
                                                   evo.project_dep.baseDir, evo.project_dep)
            test_result_parent_test_suite = self.run_test_suite(evo.project_dep.parentReg, input.targets,
                                                                evo.project_dep.parentReg, evo.project_dep)
        except:
            print("Some project versions could not be evaluated")
            conflict_info.append(["NONE", set(), "NO-INFORMATION", commitOne, commitTestSuite, "",
                                  tool])

        return path_suite, test_result_base, test_result_parent_test_suite

    def check_semantic_conflict_occurrence(self, path_suite, test_result_base, test_result_parent_test_suite,
                                    test_result_other_parent, test_result_merge, commitBaseSha, commitParentTestSuite,
                                    commitOtherParent, commitMergeSha, tool, conflict_info):

        conflict_info.append(self.behaviour_change.check_conflict_occurrence_for_first_criterion(test_result_base,
                                    test_result_parent_test_suite, test_result_merge, path_suite, commitBaseSha,
                                    commitParentTestSuite, commitMergeSha, tool))
        conflict_info.append(self.behaviour_change.check_conflict_occurrence_for_second_criterion(test_result_base,
                                    test_result_parent_test_suite, test_result_other_parent, test_result_merge, path_suite,
                                    commitBaseSha, commitParentTestSuite, commitOtherParent, commitMergeSha, tool))

    def check_behavior_change_commit_pair(self, path_suite, test_result_base, test_result_parent_test_suite, test_result_merge,
                                    commitBaseSha, commitParentTestSuite, commitMergeSHa, tool, conflict_info):

        conflict_info.append(self.behaviour_change.check_different_test_results_for_commit_pair(test_result_base,
                                    test_result_parent_test_suite, path_suite, commitBaseSha, commitParentTestSuite, tool))
        conflict_info.append(self.behaviour_change.check_different_test_results_for_commit_pair(test_result_merge,
                                    test_result_parent_test_suite, path_suite, commitMergeSHa, commitParentTestSuite, tool))

    def run_test_suite(self, classes_dir, target_classes: "dict[str, list[str]]", mutant_dir, project_dep):
        junit = JUnit(java=project_dep.java, classpath=classes_dir)
        # For now, only collect coverage for the first class passed in
        target_class = list(target_classes.keys())[0]
        res = junit.run_with_mutant(self.test_suite, target_class, mutant_dir)
        return res

    @abstractmethod
    def generate_test_suite(self, scenario: MergeScenario, project_dep, input: MergeScenarioUnderAnalysis) -> Suite:
        pass

    def generate_and_run_test_suites_for_commit(self, evo, scenario: MergeScenario, commitOne, conflict_info, tool, input: MergeScenarioUnderAnalysis = None):
        path_suite = []
        test_result_base = set()

        try:
            path_suite = self.generate_test_suite(scenario, evo.project_dep)

            test_result_base = self.run_test_suite(evo.project_dep.parentReg, input.targets,
                                                   evo.project_dep.baseDir, evo.project_dep)
        except:
            print("Some project versions could not be evaluated")
            conflict_info.append(["NONE", set(), "NO-INFORMATION", commitOne, "",
                                  tool])

        return path_suite, test_result_base

    def run_tool_for_commit(self, evo, scenario: MergeScenario, jarCommit, commitSha, tool, projectName=None, input: MergeScenarioUnderAnalysis = None):
        conflict_info = []
        try:
            self.setup_for_partial_merge_scenario(evo, scenario, jarCommit, jarCommit, jarCommit)
            test_results_left = self.generate_and_run_test_suites_for_commit(evo, scenario, commitSha, conflict_info, tool, input)
            if (len(test_results_left[0]) > 0):
                conflict_info = test_results_left[0][1]

        except:
            print("Some project versions could not be evaluated")

        return conflict_info

    def _convert_new_suite_to_old_test_suite(self, suite: TestSuite) -> Suite:
        return Suite(
            suite_name=suite.path,
            suite_dir=suite.path,
            suite_classes_dir=os.path.join(suite.path, "classes"),
            test_classes=suite.test_classes_names
        )