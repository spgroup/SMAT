import logging
import os
from typing import List
from nimrod.core.merge_scenario_under_analysis import MergeScenarioUnderAnalysis

from nimrod.test_suite_generation.generators.test_suite_generator import \
    TestSuiteGenerator
from nimrod.tests.utils import get_config
from nimrod.tools.bin import EVOSUITE, EVOSUITE_RUNTIME


class EvosuiteTestSuiteGenerator(TestSuiteGenerator):
    def get_generator_tool_name(self) -> str:
        return "EVOSUITE"

    def _execute_tool_for_tests_generation(self, input_jar: str, output_path: str, scenario: MergeScenarioUnderAnalysis, use_determinism: bool) -> None:
        for class_name, methods in scenario.targets.items():
          logging.debug(f"Starting generation for class {class_name}")
          params = [
              '-jar', EVOSUITE,
              '-projectCP', input_jar,
              '-class', class_name,
              '-Dassertion_strategy=all',
              '-Dp_reflection_on_private=0',
              '-Dreflection_start_percent=0',
              '-Dp_functional_mocking=0',
              '-Dfunctional_mocking_percent=0',
              '-Dminimize=false',
              '-Djunit_check=false',
              '-Dinline=false',
          ]
          
          if use_determinism:
            params += ["-Dstopping_condition=MaxStatements", f"-seed={self.SEED}"]
          else:
            params += [f'-Dsearch_budget={self.SEARCH_BUDGET}']

          if(len(methods) > 0):
            params.append(
                f'-Dtarget_method_list="{self._create_method_list(methods)}"')

          self._java.exec_java(output_path, self._java.get_env(), 3000, *tuple(params))

    def _get_test_suite_class_paths(self, path: str) -> List[str]:
        paths = []

        for node in os.listdir(path):
            if os.path.isdir(os.path.join(path, node)):
                paths += self._get_test_suite_class_paths(os.path.join(path, node))
            elif node.endswith(".java"):
                paths.append(os.path.join(path, node))

        # Due to dependencies, we need to compile the Evosuite Scaffold files first.
        # This is a hack to get the scaffolding files at the begining of the list.
        return sorted(paths, key=lambda name: -1000 if name.endswith("_scaffolding.java") else 1000)

    def _get_test_suite_class_names(self, test_suite_path: str) -> List[str]:
        class_names = []

        for class_path in self._get_test_suite_class_paths(test_suite_path):
            class_fqcn = os.path.relpath(class_path, os.path.join(
                test_suite_path, "evosuite-tests")).replace(os.sep, ".")
            class_names.append(class_fqcn[:-5])

        return class_names

    # Evosuite needs to add its own Runtime in order to compile test suite
    def _compile_test_suite(self, input_jar: str, output_path: str, extra_class_path: List[str] = []) -> str:
        return super()._compile_test_suite(input_jar, output_path, [EVOSUITE_RUNTIME] + extra_class_path)

    def _create_method_list(self, methods: "List[str]"):
        rectified_methods = [self._convert_method_signature(
            method) for method in methods]
        return (":").join(rectified_methods)

    def _convert_method_signature(self, meth_signature: str) -> str:
        method_return = ""
        try:
            method_return = meth_signature.split(")")[1]
        except Exception as e:
            print(e)
        meth_name = meth_signature[:meth_signature.rfind("(")]
        meth_args = meth_signature[meth_signature.find(
            "(") + 1:meth_signature.rfind(")")].split(",")
        asm_meth_format = self._asm_based_method_method_descriptor(
            meth_args, method_return)

        return meth_name+asm_meth_format

    # See at: https://asm.ow2.io/asm4-guide.pdf -- Section 2.1.3 and 2.1.4
    # Java type Type descriptor
    # boolean Z
    # char C
    # byte B
    # short S
    # int I
    # float F
    # long J
    # double D
    # Object Ljava/lang/Object;
    # int[] [I
    # Object[][] [[Ljava/lang/Object;
    def _asm_based_method_method_descriptor(self, method_arguments, method_return):
        result = '('
        for arg in method_arguments:
            arg = arg.strip()
            result = result + self._asm_based_type_descriptor(arg)
        result = result + ')'
        result = result + self._asm_based_type_descriptor(method_return)
        return result

    def _asm_based_type_descriptor(self, arg):
        result = ''
        if '[]' in arg:
            result = result + '['
            arg = arg.replace('[]', '')

        if arg == '':
            result = result + ''
        elif arg == 'int':
            result = result + 'I'
        elif arg == 'float':
            result = result + 'F'
        elif arg == 'boolean':
            result = result + 'Z'
        elif arg == 'char':
            result = result + 'C'
        elif arg == 'byte':
            result = result + 'B'
        elif arg == 'short':
            result = result + 'S'
        elif arg == 'long':
            result = result + 'J'
        elif arg == 'double':
            result = result + 'D'
        elif arg == 'void':
            result = result + 'V'
        elif arg == 'String':
            result = result + 'Ljava/lang/String;'
        else:
            temp = "L" + arg.replace('.', '/') + ';'
            result = result + temp

        return result
