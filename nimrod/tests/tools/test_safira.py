import subprocess

from unittest import TestCase

from nimrod.tests.utils import calculator_src_aor_1
from nimrod.tests.utils import calculator_target_dir
from nimrod.tests.utils import calculator_project_dir
from nimrod.tests.utils import get_config
from nimrod.tools.java import Java
from nimrod.tools.maven import Maven
from nimrod.tools.safira import Safira


class TestSafira(TestCase):

    def setUp(self):
        self.java = Java(get_config()['java_home'])
        self.maven = Maven(self.java, get_config()['maven_home'])
        self.maven.compile(calculator_project_dir(), 10)

    '''def test_run_safira(self):
        safira = Safira(self.java, calculator_target_dir(),
                        calculator_src_aor_1())

        results = safira.run()

        self.assertEqual(3, len(results.methods))
        self.assertTrue('br.ufal.ic.easy.operations.Sum.impacted(int, int)' in
                        results.methods)
        self.assertTrue('br.ufal.ic.easy.operations.Sum.execute(int, int)' in
                        results.methods)
        self.assertTrue('br.ufal.ic.easy.Calculator.sum(int, int)' in
                        results.methods)
        self.assertEqual(2, len(results.constructors))
        self.assertTrue('br.ufal.ic.easy.Calculator()' in
                        results.constructors)
        self.assertTrue('br.ufal.ic.easy.operations.Sum()' in
                        results.constructors)'''

    def test_run_safira_timeout(self):
        safira = Safira(self.java, calculator_target_dir(),
                        calculator_src_aor_1())

        with self.assertRaises(subprocess.TimeoutExpired):
            safira.run(timeout=0)
