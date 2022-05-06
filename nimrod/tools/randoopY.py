from nimrod.tools.bin import RANDOOPY
from nimrod.tools.randoop import Randoop
from nimrod.utils import generate_classpath


# Nova versao do randoop com modificacoes (Colocar melhor descricao da diferenca do randoop)
class RandoopY(Randoop):

    def _exec_tool(self):
        params = [
            '-classpath', generate_classpath([self.classpath, RANDOOPY]),
            'randoop.main.Main',
            'gentests',
            '--randomseed=10',
            '--time-limit=300',
            '--testclass=' + self.sut_class,
            '--junit-output-dir=' + self.suite_dir
        ]

        params += self.parameters

        return self._exec(*tuple(params))
