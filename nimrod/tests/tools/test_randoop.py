from unittest import TestCase

import os
import shutil

from nimrod.tests.utils import get_config
from nimrod.tests.utils import calculator_project_dir
from nimrod.tests.utils import calculator_clean_project
from nimrod.tests.utils import calculator_target_dir
from nimrod.tests.utils import calculator_src_aor_1

from nimrod.utils import get_java_files, get_class_files
from nimrod.tools.java import Java
from nimrod.tools.maven import Maven
from nimrod.tools.randoop import Randoop
from nimrod.tools.safira import Safira


class TestRandoop(TestCase):

    def setUp(self):
        self.java_home = get_config()['java_home']
        self.maven_home = get_config()['maven_home']

        self.java = Java(self.java_home)
        self.maven = Maven(self.java, self.maven_home)

        self.maven.compile(calculator_project_dir(), 10)

    def test_generate(self):

        tests_src = os.path.join(calculator_project_dir(), 'randoop')

        randoop = Randoop(
            java=self.java,
            classpath=os.path.join(calculator_target_dir(), 'classes'),
            tests_src=tests_src,
            sut_class='br.ufal.ic.easy.operations.Sum',
            sut_classes=['br.ufal.ic.easy.operations.Sum']
        )
        randoop.parameters = ['--time-limit=1',
                              '--testclass=br.ufal.ic.easy.operations.Sum']

        (suite_name, suite_dir, suite_classes_dir,
         suite_classes) = randoop.generate()

        self.assertTrue(suite_name.startswith('randoop'))
        self.assertTrue(os.path.exists(suite_dir))

        self.assertTrue(len(get_java_files(suite_dir)) > 1)
        self.assertTrue(len(get_class_files(suite_classes_dir)) > 1)
        self.assertEqual(2, len(suite_classes))

        # shutil.rmtree(tests_src)

    def tearDown(self):
        calculator_clean_project()
