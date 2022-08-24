from enum import Enum


class TestCaseResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    FLAKY = "FLAKY"
    NOT_EXECUTABLE = "NOT_EXECUTABLE"
