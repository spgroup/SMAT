'''import os
import shutil

from unittest import TestCase

from nimrod.tools.java import Java
from nimrod.tools.maven import Maven
from nimrod.tests.utils import get_config
from nimrod.tests.utils import calculator_project_dir
from nimrod.tests.utils import calculator_mutants_dir

from nimrod.nimrod import Nimrod


class TestNimrod(TestCase):

    def setUp(self):
        self.java = Java(get_config()['java_home'])
        self.maven = Maven(self.java, get_config()['maven_home'])

    def test_nimrod(self):
        nimrod = Nimrod(self.java, self.maven)
        results = nimrod.run(calculator_project_dir(), calculator_mutants_dir(),
                             'br.ufal.ic.easy.operations.Sum',
                             randoop_params=['--time-limit=1'],
                             evosuite_params=['-Dsearch_budget=1'])

        self.assertEqual(True, results['AOI_1'].maybe_equivalent)
        self.assertEqual(False, results['AOI_1'].not_equivalent)
        self.assertTrue(len(results['AOI_1'].coverage.call_points) > 0)
        self.assertTrue(len(results['AOI_1'].coverage.test_cases) > 0)
        self.assertTrue(results['AOI_1'].coverage.executions > 0)

        self.assertEqual(False, results['AOR_1'].maybe_equivalent)
        self.assertEqual(True, results['AOR_1'].not_equivalent)
        self.assertTrue(len(results['AOR_1'].coverage.call_points) > 0)
        self.assertTrue(len(results['AOR_1'].coverage.test_cases) > 0)
        self.assertTrue(results['AOR_1'].coverage.executions > 0)

        self.assertEqual(False, results['AOR_2'].maybe_equivalent)
        self.assertEqual(True, results['AOR_2'].not_equivalent)
        self.assertTrue(len(results['AOR_2'].coverage.call_points) > 0)
        self.assertTrue(len(results['AOR_2'].coverage.test_cases) > 0)
        self.assertTrue(results['AOR_2'].coverage.executions > 0)

        shutil.rmtree(os.path.join(calculator_project_dir(), 'nimrod_output'))

    def test_nimrod_with_output_dir(self):
        nimrod = Nimrod(self.java, self.maven)
        output_dir = os.path.join(calculator_project_dir(), 'nimrod_output_2')

        results = nimrod.run(calculator_project_dir(), calculator_mutants_dir(),
                             'br.ufal.ic.easy.operations.Sum',
                             randoop_params=['--time-limit=1'],
                             evosuite_params=['-Dsearch_budget=1'],
                             output_dir=output_dir)

        shutil.rmtree(output_dir)
        self.assertEqual(3, len(results))
'''
