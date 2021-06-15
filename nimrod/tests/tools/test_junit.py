from unittest import TestCase

import os
import shutil
import subprocess

from nimrod.tests.utils import get_config
from nimrod.tests.utils import calculator_project_dir
from nimrod.tests.utils import calculator_clean_project
from nimrod.tests.utils import calculator_target_dir
from nimrod.tests.utils import calculator_mutants_dir

from nimrod.tools.java import Java
from nimrod.tools.maven import Maven
from nimrod.tools.randoop import Randoop
from nimrod.tools.junit import JUnit
from nimrod.tools.mujava import MuJava


class TestJUnit(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.java_home = get_config()['java_home']
        cls.maven_home = get_config()['maven_home']

        cls.java = Java(cls.java_home)
        cls.maven = Maven(cls.java, cls.maven_home)

        cls.maven.compile(calculator_project_dir(), 10)

        cls.classpath = os.path.join(calculator_target_dir(), 'classes')
        cls.tests_src = os.path.join(calculator_project_dir(), 'randoop')
        cls.sut_class = 'br.ufal.ic.easy.operations.Sum'

        (cls.suite_name, cls.suite_dir, cls.suite_classes_dir,
         cls.suite_classes) = cls.generate_suite(cls.java, cls.tests_src,
                                                 cls.sut_class)

    def test_run_junit(self):
        junit = JUnit(self.java, self.classpath)

        output = junit.exec(self.suite_dir, self.suite_classes_dir,
                            self.sut_class, self.suite_classes[0])

        self.assertTrue(output.ok_tests_number > 0)
        self.assertTrue(output.fail_tests == 0)
        self.assertTrue(len(output.fail_test_set) == 0)
        self.assertTrue(output.run_time > 0)

    '''def test_run_junit_timeout(self):
        junit = JUnit(self.java, self.classpath)

        with self.assertRaises(subprocess.TimeoutExpired):
            junit.exec(self.suite_dir, self.suite_classes_dir,
                       self.sut_class, self.suite_classes[0], 0)

    def test_run_junit_with_mutant(self):
        junit = JUnit(self.java, self.classpath)

        mujava = MuJava(self.java, calculator_mutants_dir())
        mutants = mujava.read_log()
        mujava.compile_mutants(self.classpath, mutants)

        output = junit.exec_with_mutant(self.suite_dir, self.suite_classes_dir,
                                        self.sut_class, self.suite_classes[0],
                                        mujava.read_log()[1])
        self.assertTrue(output.ok_tests > 0)
        self.assertTrue(output.fail_tests > 0)
        self.assertTrue(len(output.fail_test_set) > 0)
        self.assertTrue(output.run_time > 0)'''

    @staticmethod
    def generate_suite(java, tests_src, sut_class):
        randoop = Randoop(
            java=java,
            classpath=os.path.join(calculator_target_dir(), 'classes'),
            tests_src=tests_src,
            sut_class=sut_class,
            sut_classes=[sut_class]
        )
        randoop.parameters = ['--time-limit=1',
                              '--testclass=br.ufal.ic.easy.operations.Sum']

        return randoop.generate()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(os.path.join(calculator_project_dir(), 'randoop'))
        calculator_clean_project()

