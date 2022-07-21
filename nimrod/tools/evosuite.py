import os
import re

from nimrod.tools.suite_generator import SuiteGenerator
from nimrod.utils import get_class_files, get_java_files
from nimrod.tools.bin import EVOSUITE, EVOSUITE_RUNTIME
from nimrod.tools.suite_generator import Suite


class Evosuite(SuiteGenerator):
    def _get_tool_name(self):
        return "evosuite"

    def _exec_tool(self):
        for class_name, methods in self.scenario.merge_scenario.targets.items():
            params = [
                '-jar', EVOSUITE,
                '-projectCP', self.classpath,
                '-class', class_name,
                '-Dtimeout', '10000',
                '-Dassertion_strategy=all',
                '-Dp_reflection_on_private=0',
                '-Dreflection_start_percent=0',
                '-Dp_functional_mocking=0',
                '-Dfunctional_mocking_percent=0',
                '-Dminimize=false',
                '-Dsearch_budget=30',
                '-Djunit_check=false',
                '-Dinline=false',
                '-DOUTPUT_DIR=' + self.suite_dir,
            ]

            if len(methods) > 0:
                params.append('-Dtarget_method_list="' +
                           self.create_method_list(methods) + '"')

            params += self.parameters
            self._exec(*tuple(params))

    def _test_classes(self):
        classes = []

        for class_file in sorted(get_class_files(self.suite_classes_dir)):
            filename, _ = os.path.splitext(class_file)
            if not filename.endswith('_scaffolding'):
                classes.append(filename.replace(os.sep, '.'))

        return classes

    def _get_suite_dir(self):
        return os.path.join(self.suite_dir, 'evosuite-tests')

    @staticmethod
    def _extra_classpath():
        return [EVOSUITE_RUNTIME]

    def _get_java_files(self):
        ordered_files = []

        for file in sorted(get_java_files(self.suite_dir)):
            if '_scaffolding' in file:
                ordered_files.insert(0, file)
            else:
                ordered_files.append(file)

        return ordered_files

    def _exec_differential(self, mutants_classpath):
        params = [
            '-jar', EVOSUITE,
            '-regressionSuite',
            '-projectCP', self.classpath,
            '-Dregressioncp=' + mutants_classpath,
            '-class', self.sut_class,
            '-DOUTPUT_DIR=' + self.suite_dir
        ]

        params += self.parameters

        return self._exec(*tuple(params))

    def generate_differential(self, mutant_classpath, make_dir=True):
        if make_dir:
            self._make_src_dir()
        self._exec_differential(mutant_classpath)
        self._compile()

        return Suite(suite_name=self.suite_name, suite_dir=self.suite_dir,
                     suite_classes_dir=self.suite_classes_dir,
                     test_classes=self._test_classes())

    def get_format_evosuite_method_name(self):
        method_name = ""
        try:
            pattern = re.compile("\.[a-zA-Z0-9\-\_]*\([\s\S]*")
            result = pattern.search(self.sut_method)
            method_name = result.group(0)[1:]
        except Exception as e:
            print(e)
            method_name = self.sut_method

        return method_name

    def create_method_list(self, methods: "list[str]"):
        rectified_methods = [self.convert_method_signature(
            method) for method in methods]
        return (":").join(rectified_methods)

    def convert_method_signature(self, meth_signature: str) -> str:
        method_return = ""
        try:
            method_return = meth_signature.split(")")[1]
        except Exception as e:
            print(e)
        meth_name = meth_signature[:meth_signature.rfind("(")]
        meth_args = meth_signature[meth_signature.find(
            "(") + 1:meth_signature.rfind(")")].split(",")
        asm_meth_format = self.asm_based_method_method_descriptor(
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
    def asm_based_method_method_descriptor(self, method_arguments, method_return):
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
