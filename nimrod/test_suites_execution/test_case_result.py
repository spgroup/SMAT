from enum import Enum


class TestCaseResult(str, Enum):
    __test__ = False

    PASS = "PASS"
    FAIL = "FAIL"
    FLAKY = "FLAKY"
    NOT_EXECUTABLE = "NOT_EXECUTABLE"
