import logging
import os
import json
import shutil

PATH = os.path.dirname(os.path.abspath(__file__))


def get_config() -> "dict[str, str]":
    with open(os.path.join(PATH, os.sep.join(['env-config.json'])), 'r') as j:
        j = json.loads(j.read())

    return j


def calculator_project_dir():
    return os.path.join(PATH, 'example')


def calculator_package():
    return 'br.ufal.ic.easy'


def calculator_src_dir():
    return os.path.join(calculator_project_dir(), 'src', 'main', 'java')


def calculator_package_dir():
    return os.path.join(calculator_src_dir(), 'br', 'ufal', 'ic', 'easy')


def calculator_java_file():
    return os.path.join(calculator_package_dir(), 'Calculator.java')


def calculator_operation_java_file():
    return os.path.join(calculator_package_dir(), 'operations',
                        'Operation.java')


def calculator_target_dir():
    return os.path.join(calculator_project_dir(), 'target')


def calculator_clean_project():
    target_dir = calculator_target_dir()

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)


def calculator_mutants_dir():
    return os.path.join(calculator_project_dir(), 'mutants')


def calculator_mutants_log():
    return os.path.join(calculator_mutants_dir(), 'mutation_log')


def calculator_sum_original():
    return os.path.join(calculator_package_dir(), 'operations',
                        'Sum.java')


def calculator_src_aor_1():
    return os.path.join(calculator_mutants_dir(), 'AOR_1')


def calculator_sum_aor_1():
    return os.path.join(calculator_src_aor_1(), 'br', 'ufal', 'ic', 'easy',
                        'operations', 'Sum.java')


def setup_logging():
    config = get_config()
    config_level = config.get('logger_level')
    level = logging._nameToLevel[config_level] if config_level else logging.INFO
    logging.basicConfig(level=level)
