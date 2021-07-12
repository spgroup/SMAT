from nimrod.tools.bin import JACOCOCLI, JACOCOAGENT, JUNIT, HAMCREST
from nimrod.utils import generate_classpath


class Jacoco:
    def __init__(self, java):
        self.java = java

    # Run java -jar jacococli.jar instrument project_jar --dest dest_jar_instrumented
    def execInstrumentJar(self, projectJar, destJarinstrumented):
        params = [
            '-jar', JACOCOCLI,
            'instrument', projectJar,
            '--dest', destJarinstrumented
        ]
        return self.execJava(*params)

    # projectJar = jar instrumentado do projeto
    # suite_class = local do arquivo class da suite de testes
    # test_class = nome da classe de teste
    def createJacocoExec(self, projectJar, suite_class, test_class):
        classpath = generate_classpath([
            JUNIT, HAMCREST, JACOCOAGENT,
            suite_class, projectJar
        ])
        params = (
            '-classpath', classpath,
            'org.junit.runner.JUnitCore', test_class
        )

        return self.execJava(*params)

    # jacocoExecDir = local do arquivo jacocoExec
    # classFiles = local do arquivo class da classe alvo dos testes.
    # nameCsvFile = nome do arquivo csv gerado com o report dos testes.
    def generateReport(self, jacocoExecDir, classFiles, nameCsvFile):
        params = [
            '-jar', JACOCOCLI,
            'report', jacocoExecDir,
            '--classfiles', classFiles,
            '--csv', nameCsvFile
        ]

        return self.execJava(*params)

    # caminhoJacocoExec = local do arquivo jacocoExec
    # classFiles = local do arquivo class da classe alvo dos testes.
    # localHtmlGerado = arquivo para criacao do report html.
    def generateReportHtml(self, jacocoExecDir, classFiles):
        novoClassFile = classFiles
        if type(classFiles) == list: # tratamento para caso receber uma lista de jars
            novoClassFile = ""
            for i in range(len(classFiles)):
                novoClassFile = novoClassFile + classFiles[i]
        caminhoJacocoExec = jacocoExecDir + "/jacoco.exec"
        localHtmlGerado = jacocoExecDir + "/report"
        params = [
            '-jar', JACOCOCLI,
            'report', caminhoJacocoExec,
            '--classfiles', novoClassFile,
            '--html', localHtmlGerado
        ]

        return self.execJava(*params)

    def execJava(self, *params):
        return self.java.simple_exec_java(*params)
