from nimrod.tools.suite_generator import SuiteGenerator
from nimrod.tools.randoop import Randoop
import os

from nimrod.utils import generate_classpath
from nimrod.tools.bin import MOD_RANDOOP


METHOD_LIST_FILENAME = 'methods_to_test.txt'
TARGET_CLASS_LIST_FILENAME = 'classes_to_test.txt'


class Randoop_Modified(SuiteGenerator):

    def _get_tool_name(self):
        return "randoop-modified"

    def _exec_tool(self):
        params = [
            '-classpath', generate_classpath([self.classpath, MOD_RANDOOP]),
            'randoop.main.Main',
            'gentests',
            '--randomseed=10',
            '--time-limit=10',
            '--junit-output-dir=' + self.suite_dir
        ]

        params += self.parameters

        return self._exec(*tuple(params))

    def _test_classes(self):
        return ['RegressionTest', 'ErrorTest']

    def generate_with_impact_analysis(self):
        self._make_src_dir()
        class_list = self.create_target_classes_list()
        method_list = self.create_target_methods_list()

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

    def create_target_classes_list(self, filename=TARGET_CLASS_LIST_FILENAME) -> str:
        filename = os.path.join(self.suite_dir, filename)

        with open(filename, 'w') as f:
            fqcns = self.input.targets.keys()
            [f.write(fqcn.replace(" ", "") + "\n") for fqcn in fqcns]
            f.close()

        return filename

    def create_target_methods_list(self, filename=METHOD_LIST_FILENAME) -> str:
        filename = os.path.join(self.suite_dir, filename)

        with open(filename, 'w') as f:
            for fqcn, methods in self.input.targets.items():
                for method in methods:
                    method_signature = fqcn + "." + method
                    f.write(method_signature)

        return filename
