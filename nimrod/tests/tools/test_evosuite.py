from unittest import TestCase

import os
import shutil
from nimrod.input_parsing.smat_input import SmatInput
from nimrod.project_info.merge_scenario import MergeScenario

from nimrod.tests.utils import get_config
from nimrod.tests.utils import calculator_project_dir
from nimrod.tests.utils import calculator_clean_project
from nimrod.tests.utils import calculator_target_dir
from nimrod.tests.utils import calculator_mutants_dir

from nimrod.utils import get_java_files, get_class_files
from nimrod.tools.java import Java
from nimrod.tools.maven import Maven
from nimrod.tools.evosuite import Evosuite
from nimrod.tools.mujava import MuJava

class TestEvosuite(TestCase):

    def setUp(self):
        self.java_home = get_config()['java_home']
        self.maven_home = get_config()['maven_home']

        self.java = Java(self.java_home)
        self.maven = Maven(self.java, self.maven_home)

        self.maven.compile(calculator_project_dir(), 10)

    def test_generate(self):

        tests_src = os.path.join(calculator_project_dir(), 'evosuite')

        evosuite = Evosuite(
            java=self.java,
            classpath=os.path.join(calculator_target_dir(), 'classes'),
            tests_src=tests_src,
            sut_class='br.ufal.ic.easy.operations.Sum',
            params=['-Dsearch_budget=1'],
            input=SmatInput(targets={'br.ufal.ic.easy.operations.Sum': []})
        )

        (suite_name, suite_dir, suite_classes_dir,
         suite_classes) = evosuite.generate()

        self.assertTrue(suite_name.startswith('evosuite'))
        self.assertTrue(os.path.exists(suite_dir))

        self.assertTrue(len(get_java_files(suite_dir)) > 1)
        self.assertTrue(len(get_class_files(suite_classes_dir)) > 1)
        self.assertEquals(1, len(suite_classes))

        shutil.rmtree(tests_src)

    def test_generate_differential(self):

        tests_src = os.path.join(calculator_project_dir(), 'evosuite')

        evosuite = Evosuite(
            java=self.java,
            classpath=os.path.join(calculator_target_dir(), 'classes'),
            tests_src=tests_src,
            sut_class='br.ufal.ic.easy.operations.Sum',
            params=['-Dsearch_budget=1'],
            input=SmatInput(targets={'br.ufal.ic.easy.operations.Sum': []})
        )

        mutants = MuJava(java=self.java,
                         mutants_dir=calculator_mutants_dir()).read_log()

        (suite_name, suite_dir, suite_classes_dir,
         suite_classes) = evosuite.generate_differential(mutants[1].dir)

        self.assertTrue(suite_name.startswith('evosuite'))
        self.assertTrue(os.path.exists(suite_dir))

        self.assertTrue(len(get_java_files(suite_dir)) > 1)
        self.assertTrue(len(get_class_files(suite_classes_dir)) > 1)
        self.assertEquals(1, len(suite_classes))

        shutil.rmtree(tests_src)

    def tearDown(self):
        calculator_clean_project()
