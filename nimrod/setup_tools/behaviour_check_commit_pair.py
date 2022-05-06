from nimrod.setup_tools.behaviour_check import Behaviour_check

class Behavior_check_commit_pair(Behaviour_check):

    def check_different_test_results_for_commit_pair(self, parent_one, parent_two, path_suite, commitOneSHA, commitTwoSHA, tool):
        results = super().check_different_test_results_for_commit_pair(parent_one, parent_two, path_suite, commitOneSHA, commitTwoSHA, tool);

        return [results[0], results[1], path_suite[1], "BEHAVIOR_CHANGE_COMMIT_PAIR", commitOneSHA, commitTwoSHA, tool,
                results[9]]