import logging
from typing import Dict, List
from nimrod.dynamic_analysis.behavior_change_checker import BehaviorChangeChecker
from nimrod.dynamic_analysis.criteria.first_semantic_conflict_criteria import FirstSemanticConflictCriteria
from nimrod.dynamic_analysis.criteria.second_semantic_conflict_criteria import SecondSemanticConflictCriteria
from nimrod.dynamic_analysis.main import DynamicAnalysis
from nimrod.input_parsing.smat_input import SmatInput
from nimrod.smat import SMAT
from nimrod.test_suite_generation.main import TestSuiteGeneration
from nimrod.tests.utils import setup_logging, get_config
from nimrod.test_suite_generation.generators.test_suite_generator import TestSuiteGenerator
from nimrod.test_suite_generation.generators.randoop_test_suite_generator import RandoopTestSuiteGenerator
from nimrod.test_suite_generation.generators.evosuite_differential_test_suite_generator import EvosuiteDifferentialTestSuiteGenerator
from nimrod.test_suite_generation.generators.evosuite_test_suite_generator import EvosuiteTestSuiteGenerator
from nimrod.test_suites_execution.main import TestSuitesExecution, TestSuiteExecutor
from nimrod.tools.bin import MOD_RANDOOP, RANDOOP
from nimrod.tools.java import Java
from nimrod.input_parsing.input_parser import CsvInputParser, JsonInputParser


def get_test_suite_generators(config: Dict[str, str]) -> List[TestSuiteGenerator]:
  config_generators = config.get(
      'test_suite_generators', 'randoop,randoop-modified,evosuite,evosuite-differential')
  generators = list()

  if 'randoop' in config_generators:
    generators.append(RandoopTestSuiteGenerator(Java(), RANDOOP, "RANDOOP"))
  if 'randoop-modified' in config_generators:
    generators.append(RandoopTestSuiteGenerator(
        Java(), MOD_RANDOOP, "RANDOOP_MODIFIED"))
  if 'evosuite' in config_generators:
    generators.append(EvosuiteTestSuiteGenerator(Java()))
  if 'evosuite-differential' in config_generators:
    generators.append(EvosuiteDifferentialTestSuiteGenerator(Java()))

  return generators


def parse_scenarios_from_input(config: Dict[str, str]) -> List[SmatInput]:
    if config.get('input_path'):
        return JsonInputParser().parse_input(config.get('input_path'))
    elif config.get('path_hash_csv'):
        logging.WARN(
            'DEPRECATED: Providing input data with `path_hash_csv` is deprecated and will be removed in future versions of SMAT. Use `input_path` instead.')
        return CsvInputParser().parse_input(config.get('path_hash_csv'))
    else:
        logging.FATAL('Non input file provided')
        exit(1)


def main():
  setup_logging()
  config = get_config()
  test_suite_generators = get_test_suite_generators(config)
  test_suite_generation = TestSuiteGeneration(test_suite_generators)
  test_suites_execution = TestSuitesExecution(TestSuiteExecutor(Java()))
  dynamic_analysis = DynamicAnalysis([
      FirstSemanticConflictCriteria(),
      SecondSemanticConflictCriteria()
  ], BehaviorChangeChecker())

  smat = SMAT(test_suite_generation, test_suites_execution, dynamic_analysis)
  scenarios = parse_scenarios_from_input(config)

  for scenario in scenarios:
    if scenario.run_analysis:
      smat.run_tool_for_semmantic_conflict_detection(scenario)


if __name__ == '__main__':
  main()
