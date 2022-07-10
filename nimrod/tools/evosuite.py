import os
import re

from nimrod.tools.suite_generator import SuiteGenerator
from nimrod.utils import get_class_files, get_java_files
from nimrod.tools.bin import EVOSUITE, EVOSUITE_RUNTIME
from nimrod.tools.suite_generator import Suite

METHOD_LIST_FILENAME = 'methods_to_test.txt'

class Evosuite(SuiteGenerator):

    def _get_tool_name(self):
        return "evosuite"

    def _exec_tool(self):
        calls = []

        for sut_class in self.sut_classes:
            params = [
                '-jar', EVOSUITE,
                '-projectCP', self.classpath,
                '-class', sut_class,
                '-Dtimeout', '10000',
                '-Dassertion_strategy=all',
                '-Dp_reflection_on_private=0',
                '-Dreflection_start_percent=0',
                '-Dp_functional_mocking=0',
                '-Dfunctional_mocking_percent=0',
                '-Dminimize=false',
                '-Dsearch_budget=300',
                '-Djunit_check=false',
                '-Dinline=false',
                '-DOUTPUT_DIR=' + self.suite_dir
            ]

            params += self.parameters

            calls.append(self._exec(*tuple(params)))

        return calls

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

    # Argument for using only specific methods to test
    # Eg.: -Dtarget_method_list="append(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"
    def generate_with_impact_analysis(self, impact_analysis, method_analysis):
        self._make_src_dir()
        impact_analysis_result = impact_analysis.run()
        if (method_analysis):
            self.parameters.append('-Dtarget_method=\"' + self.create_method_list_for_single_method(self.get_format_evosuite_method_name()) + '\"')
        else:
            method_list = self.create_method_list(impact_analysis_result)
            if method_list.strip() != '':
                self.parameters.append('-Dtarget_method_list=\"' + method_list + '\"')

        return super().generate(make_dir=False)

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

    def create_method_list(self, impact_analysis_result):
        method_list = '' 
        for meth in impact_analysis_result.methods:
            if self.sut_class in meth:
                meth_temp = meth.replace(self.sut_class, "")[1:]
                all_methods = impact_analysis_result.all_methods_by_class[self.sut_class]
                method_with_return = [m for m in all_methods if meth_temp in m]
                if len(method_with_return) == 1:
                    m = method_with_return[0]                
                    ret = m[0:m.index(meth_temp)].strip()
                    ret = ret[ret.index(" "):].strip() 
                    meth_name = meth_temp[meth_temp.find(".")+1:meth_temp.rfind("(")]
                    meth_args = meth_temp[meth_temp.find("(")+1:meth_temp.rfind(")")].split("|")
                    asm_meth_format = self.asm_based_method_method_descriptor(meth_args, ret)
                    method_list = method_list + "{0}{1}".format(meth_name, asm_meth_format) + ":"
                    
        return method_list[:-1]

    def create_method_list_for_single_method(self, method_name):
        method_return = ""
        try:
            method_return = method_name.split(")")[1]
        except Exception as e:
            print(e)
        meth_name = method_name[method_name.find(".") + 1:method_name.rfind("(")]
        meth_args = method_name[method_name.find("(") + 1:method_name.rfind(")")].split(",")
        asm_meth_format = self.asm_based_method_method_descriptor(meth_args, method_return)
        method_list = meth_name+asm_meth_format+":"

        return method_list[:-1]

    #See at: https://asm.ow2.io/asm4-guide.pdf -- Section 2.1.3 and 2.1.4
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
    def asm_based_method_method_descriptor(self, args, ret):
        result = '('
        for arg in args:
            arg = arg.strip()
            result = result + self._asm_based_type_descriptor(arg)
        result = result + ')'
        result = result + self._asm_based_type_descriptor(ret)
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