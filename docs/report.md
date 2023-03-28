# Report Generation in SMAT
SMAT generates several reports based on different metrics, supported by its current version. In this document, initially, we discuss about `semantic_conflicts.json`, which holds the information about semantic conflict detection.

## Semantic Conflict Occurrence
In this report file, SMAT informs about the detection of semantic conflicts based on a set of interference criteria. Each entry in the `JSON` report file represents a test case that detects a single conflict. The following attributes are associated with each entry:

### project_name
This attribute refers to the `project` under analysis, which holds the merge scenario given as input, previously informed on the [nimrod/tests/env-config.json](../nimrod/tests/env-config.json) file.

### scenario_commits
This attribute shows the list of commits associated with a merge scenario, used during the generation and execution of test suites. For this current version of SMAT, only `left` and `right` are used to generate test suites, while all of them (`base`, `left`, `right`, and `merge`) are used to execute the tests on them. This list of commits is also previously informed on the [nimrod/tests/env-config.json](../nimrod/tests/env-config.json) file.

### criteria
This attribute refers to the interference criterion responsible for detecting the conflict. The possible values here are `FirstSemanticConflictCriteria` and `SecondSemanticConflictCriteria`.

### test_case_name
This attribute refers to the generated test case that detects the reported conflict. It is composed by the name of the test class and test case.

### test_case_results
This attribute indicates whether the test case responsible for the conflict detection passed or failed for each commit in `scenario_commits`. This way, the possible values for this attribute are `PASS` or `FAIL`.

### test_suite_path
This attribute informs the local path where the generated test suite is located. This test suite also holds the test case responsible for the conflict detection, see `test_case_name`

### scenario_targets
This attribute refers to the target classes and methods given as input in order to drive the generation of test suites, previously informed on the [nimrod/tests/env-config.json](../nimrod/tests/env-config.json) file. Different classes can be informed, as also different methods of the same class.

### exercised_targets
Based on the list of `scenario_targets`, as previously presented, this attribute informs the target classes and methods that are covered by the test case that detected the conflict, see `test_case_name`
