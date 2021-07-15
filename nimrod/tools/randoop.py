from nimrod.tools.suite_generator import SuiteGenerator

import os
import random

from nimrod.utils import generate_classpath
from nimrod.tools.bin import RANDOOP
from nimrod.tools.bin import MOD_RANDOOP


METHOD_LIST_FILENAME = 'methods_to_test.txt'
TARGET_CLASS_LIST_FILENAME = 'classes_to_test.txt'


class Randoop(SuiteGenerator):

    def _get_tool_name(self):
        return "randoop"

    def _exec_tool(self):
        params = [
            '-classpath', generate_classpath([self.classpath, RANDOOP]),
            'randoop.main.Main',
            'gentests',
            '--randomseed=10',
            '--time-limit=300',
            '--junit-output-dir=' + self.suite_dir
        ]

        params += self.parameters

        return self._exec(*tuple(params))

    def _test_classes(self):
        return ['RegressionTest', 'ErrorTest']

    def generate_with_impact_analysis(self, impact_analysis, method_analysis=False):
        method_list = ""
        self._make_src_dir()
        impact_analysis_result = impact_analysis.run()
        class_list = self.create_target_class_list(self.suite_dir)
        if (method_analysis):
            method_list = self.create_method_list_for_one_single_method(impact_analysis_result, self.suite_dir)
        else:
            method_list = self.create_method_list(impact_analysis_result, self.suite_dir)

        if os.path.exists(method_list):
            elem = [x for x in self.parameters if '--methodlist=' in x]
            if len(elem) > 0:
                self.parameters.remove(elem[0])
            self.parameters.append('--methodlist=' + method_list)

        if os.path.exists(class_list):
            elem = [x for x in self.parameters if '--classlist=' in x]
            if len(elem) > 0:
                self.parameters.remove(elem[0])
            self.parameters.append('--classlist=' + class_list)

        return super().generate(make_dir=False)

    
    def create_target_class_list(self, output_dir,
                           filename=TARGET_CLASS_LIST_FILENAME):
        filename = os.path.join(output_dir, filename)

        with open(filename, 'w') as f:
            methods = self.sut_classes
            [f.write(l.replace(" ","") + "\n") for l in methods]
            f.close()

        return filename

    def create_method_list(self, impact_analysis_result, output_dir,
                           filename=METHOD_LIST_FILENAME):
        filename = os.path.join(output_dir, filename)

        with open(filename, 'w') as f:
            methods = (impact_analysis_result.constructors
                       + impact_analysis_result.methods)
            [f.write(l + '\n') for l in methods]
            f.close()

        return filename

    def create_method_list_for_one_single_method(self, impact_analysis_result, output_dir,
                           filename=METHOD_LIST_FILENAME):
        filename = os.path.join(output_dir, filename)

        with open(filename, 'w') as f:
            method_name = self.sut_method
            try:
                method_name = [e+")" for e in self.sut_method.split(")") if e][0]
            except Exception as e:
                print(e)
            f.write(method_name)
            f.close()

        return filename