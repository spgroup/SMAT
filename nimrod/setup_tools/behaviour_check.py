class Behaviour_check:

    def check_different_test_results_for_commit_pair(self, parent_one, parent_two, path_suite, commitOneSHA, commitTwoSHA, tool):
        aux = (parent_one.fail_test_set.difference(parent_two.fail_test_set)).difference(parent_two.not_executed_test_set).union(parent_two.fail_test_set.difference(parent_one.fail_test_set)).difference(parent_one.not_executed_test_set)
        selected_cases = self.get_test_cases_with_files(aux, parent_one.fail_test_set_with_files).union(self.get_test_cases_with_files(aux, parent_two.fail_test_set_with_files))
        detected_behavior_change = False

        if len(selected_cases) > 0:
            detected_behavior_change = True

        return [detected_behavior_change, selected_cases, path_suite[1], "BEHAVIOR_CHANGE_COMMIT_PAIR", commitOneSHA, commitTwoSHA,
                "NOT-REQUIRED", "NOT-REQUIRED", tool, parent_one.flaky_test_set.intersection(parent_two.flaky_test_set)]

    def get_test_cases_with_files(self, selected_cases, test_cases_with_files):
        selected_cases_with_files = set()
        for test in selected_cases:
            for test_with_file in test_cases_with_files:
                if (test in test_with_file):
                    selected_cases_with_files.add(test_with_file)

        return selected_cases_with_files

    def check_conflict_occurrence_for_first_criterion(self, parent_one, parent_two, parent_tree, path_suite, commitBase, commitParentTestSuite, commitMerge, tool):
        aux_fail_pass_fail = (parent_one.fail_test_set.intersection(parent_tree.fail_test_set)).difference(parent_one.not_executed_test_set).difference(parent_tree.not_executed_test_set).difference(parent_two.not_executed_test_set).difference(parent_two.fail_test_set)
        aux_pass_fail_pass = (parent_one.ok_tests.intersection(parent_tree.ok_tests)).difference(parent_one.not_executed_test_set).difference(parent_tree.not_executed_test_set).difference(parent_two.not_executed_test_set).difference(parent_two.ok_tests)
        selected_cases = self.get_test_cases_with_files(aux_fail_pass_fail, parent_one.fail_test_set_with_files).union(self.get_test_cases_with_files(aux_pass_fail_pass, parent_two.fail_test_set_with_files))
        detected_behavior_change = False

        if len(selected_cases) > 0:
            detected_behavior_change = True

        return [detected_behavior_change, selected_cases, path_suite[1], "FIRST_CRITERION", commitBase, commitParentTestSuite, "NOT-REQUIRED", commitMerge, tool, parent_one.flaky_test_set]

    def check_conflict_occurrence_for_second_criterion(self, parent_base, parent_left, parent_right, parent_merge, path_suite, commitBase, commitParentTestSuite, commitParentOther, commitMerge, tool):
        not_executed_tests = parent_base.not_executed_test_set.union(parent_left.not_executed_test_set, parent_right.not_executed_test_set, parent_merge.not_executed_test_set)

        valid_base_left_right_pass = parent_base.ok_tests.intersection(parent_left.ok_tests, parent_right.ok_tests).difference(not_executed_tests, parent_base.fail_test_set, parent_left.fail_test_set, parent_right.fail_test_set)
        valid_base_left_right_fail = parent_base.fail_test_set.intersection(parent_left.fail_test_set, parent_right.fail_test_set).difference(not_executed_tests, parent_base.ok_tests, parent_left.ok_tests, parent_right.ok_tests)

        selected_cases = self.get_test_cases_with_files(valid_base_left_right_pass.difference(parent_merge.ok_tests), parent_merge.fail_test_set_with_files)
        selected_cases2 = self.get_test_cases_with_files(valid_base_left_right_fail.difference(parent_merge.fail_test_set), parent_base.fail_test_set_with_files)

        final_selected_cases = selected_cases.union(selected_cases2)
        detected_behavior_change = False

        if len(final_selected_cases) > 0:
            detected_behavior_change = True

        return [detected_behavior_change, final_selected_cases, path_suite[1], "SECOND_CRITERION", commitBase, commitParentTestSuite, commitParentOther, commitMerge, tool, parent_base.flaky_test_set]