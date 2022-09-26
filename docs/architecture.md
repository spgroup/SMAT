# Architecture

This documentation dive into details of SMAT architecture.

## Overview

Currently, this is an overview of SMAT architecture.

```mermaid
graph TD
    A[SMAT] ==> B[Test Generation]
    A ==> C[Test Execution]
    A ==> D[Test Dynamic Analysis]
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

## Test Suites Execution
This module is responsible for executin tests suites for a given merge scenario. Its public API is provided by the class `TestSuitesExecution` which exposes a method, capable of executing test suites in the versions provided.
```mermaid
classDiagram
    direction TD
    class TestSuitesExecution {
        +execute_test_suites(TestSuite[] suite, ScenarioJars jars) TestCaseExecutionInMergeScenario[]
        +execute_test_suites_with_coverage(TestSuite[] suite, ScenarioJars jars, String[] classes) TestCaseExecutionInMergeScenario[]
    }
    TestSuitesExecution --> TestSuiteExecutor
    TestSuitesExecution ..> TestCaseExecutionInMergeScenario

    class TestSuiteExecutor {
        +execute_test_suite(TestSuite suite, String jar) Map~TestCaseResult~
        +execute_test_suite_with_coverage(TestSuite suite, String jar, String[] classes) Map~TestCaseResult~
    }
    TestSuiteExecutor ..> TestCaseResult

    class TestCaseResult {
        <<enumeration>>
        PASS
        FAIL
        FLAKY
        COMPILATION_ERROR        
    }

    class TestCaseExecutionInMergeScenario {
        +TestSuite test_suite
        +String name
        +TestCaseResult base
        +TestCaseResult left
        +TestCaseResult right
        +TestCaseResult merge
    }
    TestCaseExecutionInMergeScenario --> TestCaseResult
```

## Dynamic Analysis

## Output Generation
This module is responsible for generating the reports with the results of SMAT. Each report has its own file, containing relevant information to its context.
```mermaid
classDiagram
    class OutputGenerator~T~ {
        -_generate_report_data(OutputGeneratorContext context)* T
        +write_report(OutputGeneratorContext context) void
    }

    class SemanticConflictsOutputGenerator~SemanticConflictsOutput~ {
        -_generate_report_data(OutputGeneratorContext context)* SemanticConflictsOutput
    }
    SemanticConflictsOutputGenerator~SemanticConflictsOutput~ ..> SemanticConflictsOutput
    OutputGenerator~T~ <|-- SemanticConflictsOutputGenerator~SemanticConflictsOutput~
    class SemanticConflictsOutput {
        +str project_name
        +Dict[str, str] scenario_commits
        +str criteria
        +str test_case_name
        +Dict[str, str] test_case_results
        +str test_suite_path
        +Dict[str, List[str]] scenario_targets
        +Dict[str, List[str]] exercised_targets
    }

    class BehaviorChangesOutputGenerator~BehaviorChangesOutput~ {
        -_generate_report_data(OutputGeneratorContext context)* BehaviorChangesOutput
    }
    BehaviorChangesOutputGenerator~BehaviorChangesOutput~ ..> BehaviorChangesOutput
    OutputGenerator~T~ <|-- BehaviorChangesOutputGenerator~BehaviorChangesOutput~
    class BehaviorChangesOutput {
        +str project_name
        +Dict[str, str] scenario_commits
        +str test_case_name
        +Dict[str, str] test_case_results
        +str test_suite_path
        +Tuple[str, str] between
    }

    class TestSuitesOutputGenerator~TestSuitesOutput~ {
        -_generate_report_data(OutputGeneratorContext context)* TestSuitesOutput
    }
    TestSuitesOutputGenerator~TestSuitesOutput~ ..> TestSuitesOutput
    OutputGenerator~T~ <|-- TestSuitesOutputGenerator~TestSuitesOutput~
    class TestSuitesOutput {
        +str project_name
        +str generator_name
        +str path
        +bool detected_semantic_conflicts
        +bool detected_behavior_changes_between_pairs
    }
```

### Trade-offs
- Since there is many information which can be needed to build all the reports available, in order to preserve all generators with the same interface, the data has been encapsulated in a Context object, which is passed into each generator.
```mermaid
classDiagram
    class OutputGeneratorContext {
        +MergeScenarioUnderAnalysis scenario
        +TestSuite[] test_suites
        +TestCaseExecutionInMergeScenario[] test_case_executions
        +SemanticConflict[] semantic_conflicts
        +BehaviorChange[] behavior_changes
    }
```
- In order to generate Semantic Conflicts reports, it was required to re-execute some of the test cases using coverage collection. Thus, in  `SemanticConflictOutputGenerator` there's a dependency with the `TestSuitesExecution` module. This coupling has been discussed to be acceptable within the project.
