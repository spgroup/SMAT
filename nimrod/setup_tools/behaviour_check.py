class Behaviour_check:

    def check_different_test_results_for_commit_pair(self, parent_one, parent_two, path_suite, commitOneSHA, commitTwoSHA, tool):
        behavior_change = (parent_one.fail_test_set.difference(parent_two.fail_test_set)).difference(parent_two.not_executed_test_set).union(parent_two.fail_test_set.difference(parent_one.fail_test_set)).difference(parent_one.not_executed_test_set)
        selected_cases_fail = self.get_test_cases_with_files(behavior_change, parent_one.fail_test_set_with_files).union(self.get_test_cases_with_files(behavior_change, parent_two.fail_test_set_with_files))
        behavior_change_error = (parent_one.fail_test_set_error.difference(parent_two.fail_test_set_error)).difference(parent_two.not_executed_test_set_error).union(parent_two.fail_test_set_error.difference(parent_one.fail_test_set_error)).difference(parent_one.not_executed_test_set_error)
        selected_cases_error = self.get_test_cases_with_files(behavior_change_error, parent_one.fail_test_set_with_files_error).union(self.get_test_cases_with_files(behavior_change_error, parent_two.fail_test_set_with_files_error))
        detected_behavior_change = False

        selected_cases = selected_cases_fail.union(selected_cases_error)
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
        aux_fail_pass_fail_reg = (parent_one.fail_test_set.intersection(parent_tree.fail_test_set)).difference(parent_one.not_executed_test_set).difference(parent_tree.not_executed_test_set).difference(parent_two.not_executed_test_set).difference(parent_two.fail_test_set)
        aux_pass_fail_pass = (parent_one.ok_tests.intersection(parent_tree.ok_tests)).difference(parent_one.not_executed_test_set).difference(parent_tree.not_executed_test_set).difference(parent_two.not_executed_test_set).difference(parent_two.ok_tests)
        selected_cases_reg = self.get_test_cases_with_files(aux_fail_pass_fail_reg, parent_one.fail_test_set_with_files).union(self.get_test_cases_with_files(aux_pass_fail_pass, parent_two.fail_test_set_with_files))

        aux_fail_pass_fail_error = (parent_one.fail_test_set_error.intersection(parent_tree.fail_test_set_error)).difference(parent_one.not_executed_test_set_error).difference(parent_tree.not_executed_test_set_error).difference(parent_two.not_executed_test_set_error).difference(parent_two.fail_test_set_error)
        selected_cases_fail_pass_fail_error = self.get_test_cases_with_files(aux_fail_pass_fail_error, parent_one.fail_test_set_with_files_error).union(self.get_test_cases_with_files(aux_fail_pass_fail_error, parent_two.fail_test_set_with_files_error))
        aux_pass_fail_pass_error = (parent_one.ok_tests_error.intersection(parent_tree.ok_tests_error)).difference(parent_one.not_executed_test_set_error).difference(parent_tree.not_executed_test_set_error).difference(parent_two.not_executed_test_set_error).difference(parent_two.ok_tests_error)
        selected_cases_pass_fail_pass_error = self.get_test_cases_with_files(aux_pass_fail_pass_error, parent_one.fail_test_set_with_files_error).union(self.get_test_cases_with_files(aux_pass_fail_pass_error, parent_two.fail_test_set_with_files_error))

        detected_behavior_change = False

        selected_cases = selected_cases_reg.union(selected_cases_pass_fail_pass_error, selected_cases_fail_pass_fail_error)
        if len(selected_cases) > 0:
            detected_behavior_change = True

        return [detected_behavior_change, selected_cases, path_suite[1], "FIRST_CRITERION", commitBase, commitParentTestSuite, "NOT-REQUIRED", commitMerge, tool, parent_one.flaky_test_set]

    def check_conflict_occurrence_for_second_criterion(self, parent_base, parent_left, parent_right, parent_merge, path_suite, commitBase, commitParentTestSuite, commitParentOther, commitMerge, tool):
        selected_cases_fail_fail_fail_pass, selected_cases_fail_pass_pass_pass, selected_cases_pass_fail_fail_fail, selected_cases_pass_pass_pass_fail = self.method_name_two(
            parent_base, parent_left, parent_right, parent_merge, parent_base.fail_test_set, parent_base.fail_test_set_with_files, parent_base.not_executed_test_set, parent_base.not_executed_test_set_with_files, parent_base.ok_tests,
            parent_left.fail_test_set, parent_left.fail_test_set_with_files, parent_left.not_executed_test_set, parent_left.not_executed_test_set_with_files, parent_left.ok_tests,
            parent_right.fail_test_set, parent_right.fail_test_set_with_files, parent_right.not_executed_test_set, parent_right.not_executed_test_set_with_files, parent_right.ok_tests,
            parent_merge.fail_test_set, parent_merge.fail_test_set_with_files, parent_merge.not_executed_test_set, parent_merge.not_executed_test_set_with_files, parent_merge.ok_tests)

        selected_cases_fail_fail_fail_pass_error, selected_cases_fail_pass_pass_pass_error, selected_cases_pass_fail_fail_fail_error, selected_cases_pass_pass_pass_fail_error = self.method_name_two(
            parent_base, parent_left, parent_right, parent_merge, parent_base.fail_test_set_error, parent_base.fail_test_set_with_files_error, parent_base.not_executed_test_set_error, parent_base.not_executed_test_set_with_files_error, parent_base.ok_tests_error,
            parent_left.fail_test_set_error, parent_left.fail_test_set_with_files_error, parent_left.not_executed_test_set_error, parent_left.not_executed_test_set_with_files_error, parent_left.ok_tests_error,
            parent_right.fail_test_set_error, parent_right.fail_test_set_with_files_error, parent_right.not_executed_test_set_error, parent_right.not_executed_test_set_with_files_error, parent_right.ok_tests_error,
            parent_merge.fail_test_set_error, parent_merge.fail_test_set_with_files_error, parent_merge.not_executed_test_set_error, parent_merge.not_executed_test_set_with_files_error, parent_merge.ok_tests_error)

        final_selected_cases = selected_cases_pass_pass_pass_fail.union(selected_cases_fail_fail_fail_pass, selected_cases_pass_fail_fail_fail, selected_cases_fail_pass_pass_pass,
            selected_cases_fail_fail_fail_pass_error, selected_cases_fail_pass_pass_pass_error, selected_cases_pass_fail_fail_fail_error, selected_cases_pass_pass_pass_fail_error)

        detected_behavior_change = False

        if len(final_selected_cases) > 0:
            detected_behavior_change = True

        return [detected_behavior_change, final_selected_cases, path_suite[1], "SECOND_CRITERION", commitBase, commitParentTestSuite, commitParentOther, commitMerge, tool, parent_base.flaky_test_set]

    def method_name(self, parent_base, parent_left, parent_merge, parent_right):
        not_executed_tests = parent_base.not_executed_test_set.union(parent_left.not_executed_test_set,
                                                                     parent_right.not_executed_test_set,
                                                                     parent_merge.not_executed_test_set)
        valid_base_left_right_pass = parent_base.ok_tests.intersection(parent_left.ok_tests,
                                                                       parent_right.ok_tests).difference(
            not_executed_tests, parent_base.fail_test_set, parent_left.fail_test_set, parent_right.fail_test_set)
        valid_base_left_right_fail = parent_base.fail_test_set.intersection(parent_left.fail_test_set,
                                                                            parent_right.fail_test_set).difference(
            not_executed_tests, parent_base.ok_tests, parent_left.ok_tests, parent_right.ok_tests)
        selected_cases_pass_pass_pass_fail = self.get_test_cases_with_files(
            valid_base_left_right_pass.difference(parent_merge.ok_tests), parent_merge.fail_test_set_with_files)
        selected_cases_fail_fail_fail_pass = self.get_test_cases_with_files(
            valid_base_left_right_fail.difference(parent_merge.fail_test_set), parent_base.fail_test_set_with_files)
        # final_selected_cases = selected_cases_pass_pass_pass_fail.union(selected_cases_fail_fail_fail_pass)
        valid_merge_left_right_pass = parent_merge.ok_tests.intersection(parent_left.ok_tests,
                                                                         parent_right.ok_tests).difference(
            not_executed_tests, parent_merge.fail_test_set, parent_left.fail_test_set, parent_right.fail_test_set)
        valid_merge_left_right_fail = parent_merge.fail_test_set.intersection(parent_left.fail_test_set,
                                                                              parent_right.fail_test_set).difference(
            not_executed_tests, parent_merge.ok_tests, parent_left.ok_tests, parent_right.ok_tests)
        selected_cases_pass_fail_fail_fail = self.get_test_cases_with_files(
            valid_merge_left_right_fail.difference(parent_base.fail_test_set), parent_merge.fail_test_set_with_files)
        selected_cases_fail_pass_pass_pass = self.get_test_cases_with_files(
            valid_merge_left_right_pass.difference(parent_base.ok_tests), parent_base.fail_test_set_with_files)
        return selected_cases_fail_fail_fail_pass, selected_cases_fail_pass_pass_pass, selected_cases_pass_fail_fail_fail, selected_cases_pass_pass_pass_fail

    def method_name_two(self, parent_base, parent_left, parent_right, parent_merge, base_fail_test, base_fail_test_files, base_not_executed_test_set, base_not_executed_test_set_with_files, base_ok_tests,
                            left_fail_test, left_fail_test_files, left_not_executed_test_set, left_not_executed_test_set_with_files, left_ok_tests,
                        right_fail_test, right_fail_test_files, right_not_executed_test_set, right_not_executed_test_set_with_files, right_ok_tests,
                        merge_fail_test, merge_fail_test_files, merge_not_executed_test_set, merge_not_executed_test_set_with_files, merge_ok_tests):
            not_executed_tests = base_not_executed_test_set.union(left_not_executed_test_set,
                                                                         right_not_executed_test_set,
                                                                         merge_not_executed_test_set)
            valid_base_left_right_pass = base_ok_tests.intersection(left_ok_tests,
                                                                           right_ok_tests).difference(
                not_executed_tests, base_fail_test, left_fail_test, right_fail_test)
            valid_base_left_right_fail = base_fail_test.intersection(left_fail_test,
                                                                     right_fail_test).difference(
                not_executed_tests, base_ok_tests, left_ok_tests, right_ok_tests)
            selected_cases_pass_pass_pass_fail = self.get_test_cases_with_files(
                valid_base_left_right_pass.difference(merge_ok_tests), merge_fail_test_files)
            selected_cases_fail_fail_fail_pass = self.get_test_cases_with_files(
                valid_base_left_right_fail.difference(merge_fail_test), base_fail_test_files)
            # final_selected_cases = selected_cases_pass_pass_pass_fail.union(selected_cases_fail_fail_fail_pass)
            valid_merge_left_right_pass = merge_ok_tests.intersection(left_ok_tests,
                                                                             right_ok_tests).difference(
                not_executed_tests, merge_fail_test, left_fail_test, right_fail_test)
            valid_merge_left_right_fail = merge_fail_test.intersection(left_fail_test,
                                                                       right_fail_test).difference(
                not_executed_tests, merge_ok_tests, left_ok_tests, right_ok_tests)
            selected_cases_pass_fail_fail_fail = self.get_test_cases_with_files(
                valid_merge_left_right_fail.difference(base_fail_test), merge_fail_test_files)
            selected_cases_fail_pass_pass_pass = self.get_test_cases_with_files(
                valid_merge_left_right_pass.difference(base_ok_tests), base_fail_test_files)
            return selected_cases_fail_fail_fail_pass, selected_cases_fail_pass_pass_pass, selected_cases_pass_fail_fail_fail, selected_cases_pass_pass_pass_fail