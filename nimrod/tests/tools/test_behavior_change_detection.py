from unittest import TestCase

from nimrod.setup_tools.behaviour_check import Behaviour_check
from nimrod.tools.junit import JUnitResult, Coverage


class TestBehaviorChangeDetection(TestCase):

    def test_expect_false_for_both_criteria(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #empty sets for all merge scenario commits
        executions_test_base.append(JUnitResult(set(), 0, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult(set(), 0, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult(set(), 0, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult(set(), 0, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        aux = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                           executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        aux2 = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                             executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                             "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertFalse(aux[0])
        self.assertFalse(aux2[0])

        behavior_change = behaviorChange.check_different_test_results_for_commit_pair(executions_test_base[0], executions_test_left[0],
                                                                                      ["",""], "aaa", "bbb", "Aux")
        behavior_change_merge = behaviorChange.check_different_test_results_for_commit_pair(executions_test_base[0], executions_test_left[0],
                                                                                            ["",""], "aaa", "bbb", "Aux")
        self.assertFalse(behavior_change[0])
        self.assertFalse(behavior_change_merge[0])

    def test_expect_true_for_first_criterion_fail_pass_fail(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 fails on base and merge commits but passes on left commit.
        #So a test conflict is expected to be reported by the first criterion
        #test1 was not executed on right commit, so no conflict is expected for the right commit.
        executions_test_base.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult(set(), 0, set(), set(), set(), {"test1"}, set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult(set(), 0, set(), {"test1"}, set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        conflict_for_left_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                         executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_right_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                          executions_test_right[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_second_criteria = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                                                     executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                                                     "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertTrue(conflict_for_left_first_criterion[0])
        self.assertFalse(conflict_for_right_first_criterion[0])
        self.assertFalse(conflict_for_second_criteria[0])

    def test_expect_true_for_first_criterion_pass_fail_pass(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 fails on left commit, but passes on base and merge commits.
        #So a test conflict is expected to be reported by the first criterion
        #test1 was not executed on right commit, so no conflict is expected for the right commit.
        executions_test_base.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult(set(), 0, set(), set(), set(), {"test1"}, set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        conflict_for_left_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                         executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_right_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                          executions_test_right[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_second_criteria = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                                                     executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                                                     "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertTrue(conflict_for_left_first_criterion[0])
        self.assertFalse(conflict_for_right_first_criterion[0])
        self.assertFalse(conflict_for_second_criteria[0])

    def test_expect_false_for_first_criterion_fail_fail_pass(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 fails on base and left commits but passes on merge commit.
        #So no test conflict is expected to be reported by the first criterion
        #test1 was not executed on right commit, so no conflict is expected for the right commit.
        executions_test_base.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult(set(), 0, set(), set(), set(), {"test1"}, set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        conflict_for_left_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                         executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_right_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                          executions_test_right[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_second_criteria = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                                                     executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                                                     "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertFalse(conflict_for_left_first_criterion[0])
        self.assertFalse(conflict_for_right_first_criterion[0])
        self.assertFalse(conflict_for_second_criteria[0])

    def test_expect_false_for_first_criterion_pass_pass_fail(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 passes on base and left commits, but fails on merge commit.
        #So no test conflict is expected to be reported by the first criterion
        #test1 was not executed on right commit, so no conflict is expected for the right commit.
        executions_test_base.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult(set(), 0, set(), set(), set(), {"test1"}, set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        conflict_for_left_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                         executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_right_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                          executions_test_right[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_second_criteria = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                                                     executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                                                     "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertFalse(conflict_for_left_first_criterion[0])
        self.assertFalse(conflict_for_right_first_criterion[0])
        self.assertFalse(conflict_for_second_criteria[0])

    def test_expect_false_for_first_criterion_fail_fail_fail(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 fails on base, left, and merge commits.
        #So no test conflict is expected to be reported by the first criterion
        #test1 was not executed on right commit, so no conflict is expected for the right commit.
        executions_test_base.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult(set(), 0, set(), set(), set(), {"test1"}, set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        conflict_for_left_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                         executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_right_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                          executions_test_right[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_second_criteria = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                                                     executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                                                     "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertFalse(conflict_for_left_first_criterion[0])
        self.assertFalse(conflict_for_right_first_criterion[0])
        self.assertFalse(conflict_for_second_criteria[0])

    def test_expect_false_for_first_criterion_pass_pass_pass(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 passes on all merge scenario commits.
        #So no test conflict is expected to be reported by the criteria
        executions_test_base.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        conflict_for_left_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                         executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_right_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                          executions_test_right[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_second_criteria = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                                                     executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                                                     "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertFalse(conflict_for_left_first_criterion[0])
        self.assertFalse(conflict_for_right_first_criterion[0])
        self.assertFalse(conflict_for_second_criteria[0])

    def test_expect_false_for_first_criterion_not_executed(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 passes on base and merge commits, but it was not executed on left and right commits.
        #So no test conflict is expected to be reported by the first criterion
        executions_test_base.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult(set(), 0, set(), set(), set(), {"test1"}, set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult(set(), 0, set(), set(), set(), {"test1"}, set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        conflict_for_left_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                         executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_right_first_criterion = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                                                          executions_test_right[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        conflict_for_second_criteria = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                                                     executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                                                     "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertFalse(conflict_for_left_first_criterion[0])
        self.assertFalse(conflict_for_right_first_criterion[0])
        self.assertFalse(conflict_for_second_criteria[0])

    def test_expect_true_for_second_criterion_fail_fail_fail_pass(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 fails on base, left and right commits but passes on merge commit.
        #So a test conflict is expected to be reported by the second criterion
        executions_test_base.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        aux = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                           executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        aux2 = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                             executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                             "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertFalse(aux[0])
        self.assertTrue(aux2[0])

    def test_expect_true_second_criterion_pass_pass_pass_fail(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 passes on base, left and right commits but fails on merge commit.
        #So a test conflict is expected to be reported by the second criterion
        executions_test_base.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        #parent_one, parent_two, parent_tree, path_suite, commitBase, commitParentTestSuite, commitMerge, tool
        aux = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                           executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        #parent_base, parent_left, parent_right, parent_merge, path_suite, commitBase, commitParentTestSuite, commitParentOther, commitMerge, tool
        aux2 = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                             executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                             "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertFalse(aux[0])
        self.assertTrue(aux2[0])

        #parent_one, parent_two, path_suite, commitOneSHA, commitTwoSHA, tool
        behavior_change = behaviorChange.check_different_test_results_for_commit_pair(executions_test_base[0], executions_test_left[0],
                                                                                      ["",""], "aaa", "bbb", "Aux")
        behavior_change_merge = behaviorChange.check_different_test_results_for_commit_pair(executions_test_merge[0], executions_test_left[0],
                                                                                            ["",""], "aaa", "bbb", "Aux")

        self.assertFalse(behavior_change[0])
        self.assertTrue(behavior_change_merge[0])

    def test_expect_false_for_second_criterion_fail_fail_fail_fail(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 fails on all merge scenario commits.
        #So no test conflict is expected to be reported by the second criterion
        executions_test_base.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult(set(), 0, set(), {"test1"}, {"RegressionText.test1()"}, set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        aux = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                           executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        aux2 = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                             executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                             "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertFalse(aux[0])
        self.assertFalse(aux2[0])

    def test_expect_false_second_criterion_pass_pass_pass_pass(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 passes on all merge scenario commits.
        #So no test conflict is expected to be reported by the second criterion
        executions_test_base.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        #parent_one, parent_two, parent_tree, path_suite, commitBase, commitParentTestSuite, commitMerge, tool
        aux = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                           executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        #parent_base, parent_left, parent_right, parent_merge, path_suite, commitBase, commitParentTestSuite, commitParentOther, commitMerge, tool
        aux2 = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                             executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                             "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertFalse(aux[0])
        self.assertFalse(aux2[0])

        #parent_one, parent_two, path_suite, commitOneSHA, commitTwoSHA, tool
        behavior_change = behaviorChange.check_different_test_results_for_commit_pair(executions_test_base[0], executions_test_left[0],
                                                                                      ["",""], "aaa", "bbb", "Aux")
        behavior_change_merge = behaviorChange.check_different_test_results_for_commit_pair(executions_test_merge[0], executions_test_left[0],
                                                                                            ["",""], "aaa", "bbb", "Aux")

        self.assertFalse(behavior_change[0])
        self.assertFalse(behavior_change_merge[0])

    def test_expect_false_second_criterion_not_executed(self):
        behaviorChange = Behaviour_check()
        executions_test_base = []
        executions_test_left = []
        executions_test_right = []
        executions_test_merge = []

        #test1 passes on base, left and right commits, but it was not executed on merge commit.
        #So a test conflict is expected to be reported by the second criterion
        executions_test_base.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_left.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_right.append(JUnitResult({"test1"}, 1, set(), set(), set(), set(), set(), set(), 0, Coverage(set(), set(), 0, dict()), False))
        executions_test_merge.append(JUnitResult(set(), 0, set(), set(), set(), {"test1"}, set(), set(), 0, Coverage(set(), set(), 0, dict()), False))

        #parent_one, parent_two, parent_tree, path_suite, commitBase, commitParentTestSuite, commitMerge, tool
        aux = behaviorChange.check_conflict_occurrence_for_first_criterion(executions_test_base[0],
                                                                           executions_test_left[0], executions_test_merge[0], ["",""], "aaa", "bbb", "ccc", "AUX");
        #parent_base, parent_left, parent_right, parent_merge, path_suite, commitBase, commitParentTestSuite, commitParentOther, commitMerge, tool
        aux2 = behaviorChange.check_conflict_occurrence_for_second_criterion(executions_test_base[0],
                                                                             executions_test_left[0], executions_test_right[0], executions_test_merge[0], ["",""],
                                                                             "aaa", "bbb", "ccc", "ddd", "AUX");

        self.assertFalse(aux[0])
        self.assertFalse(aux2[0])

        #parent_one, parent_two, path_suite, commitOneSHA, commitTwoSHA, tool
        behavior_change = behaviorChange.check_different_test_results_for_commit_pair(executions_test_base[0], executions_test_left[0],
                                                                                      ["",""], "aaa", "bbb", "Aux")
        behavior_change_merge = behaviorChange.check_different_test_results_for_commit_pair(executions_test_merge[0], executions_test_left[0],
                                                                                            ["",""], "aaa", "bbb", "Aux")

        self.assertFalse(behavior_change[0])
        self.assertFalse(behavior_change_merge[0])