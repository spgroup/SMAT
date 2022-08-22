# Architecture

This documentation dive into details of SMAT architecture.

## Overview

Currently, this is an overview of SMAT architecture.

```mermaid
graph TD
    A[SMAT] ==> B[Test Generation]
    B ==> C[Test Execution]
    B ==> D[Test Dynamic Analysis]
    A ==> E[Output Generation]
```

## Test Suite Generation
This module is responsible for generating tests suites for a given JAR. It's public API is provided by the class `TestSuiteGeneration` which exposes a single method, capable of generating test suites using the Test Suite Generators implemented in SMAT.
### Class Diagram
Following, there's the Class Diagram for this module.
```mermaid
classDiagram
    class TestSuiteGeneration {
        +generate_test_suites(SmatInput scenario, String input_jar) TestSuite[]
    }
    TestSuiteGeneration o-- TestSuiteGenerator
    TestSuiteGeneration ..> TestSuite

    class TestSuiteGenerator {
        <<interface>>
        +generate_test_suite(SmatInput scenario, String input_jar) TestSuite
    }

    class TestSuite {
        -String generator_name
        -String path
        -String[] class_path
        -String[] test_classes_names
    }
```
### Trade-offs
- The `TestSuiteGeneration` class has a dependency with the [`SmatInput`](nimrod/input_parsing/smat_input) class which provides further context information that is required by some generators (e.g.: Evosuite Differential needs to have access to the `base` JAR in order to perform the diff).

### Future improvements
- Evaluate the usage of concurrency in `TestSuiteGeneration` to allow faster generation of test suites.