import os
import filecmp
import zipfile
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
    def generateReportHtml(self, jacocoExecDir, classFiles, targetClass):
        novoClassFile = classFiles
        if type(classFiles) == list: # tratamento para caso receber uma lista de jars
            classFiles = self.adjustOnListOfJars(classFiles, targetClass)
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

    def adjustOnListOfJars(self, allJars, className):
        if (self.isListOfJarsWithTargetClass(allJars, className) == False):
            return allJars
        else:
            bestOption = ""
            firstJarWithClass = False
            for jarFile in allJars:
                if (self.isClassOnJar(jarFile, className)):
                    if (firstJarWithClass == False):
                        bestOption = jarFile
                        firstJarWithClass = True
                    else:
                        if (os.stat(bestOption).st_size < os.stat(jarFile).st_size):
                            allJars.remove(bestOption)
                            bestOption = jarFile
                        else:
                            allJars.remove(jarFile)
            return self.compareJars(allJars, className)

    def isListOfJarsWithTargetClass(self, jarFiles, className):
        numberOfJarsWithTargetClass = 0
        for jarFile in jarFiles:
            if self.isClassOnJar(jarFile, className):
                numberOfJarsWithTargetClass += 1

        if (numberOfJarsWithTargetClass > 1):
            return True
        else:
            return False

    def isClassOnJar(self, jarFile, className):
        archive = zipfile.ZipFile(jarFile, 'r')
        return className.replace(".","/")+".class" in archive.namelist()

    def compareJars(self, listOfJars, classTarget):
        bestJars = []
        for i in range(len(listOfJars)):
            for j in range(i, int(len(listOfJars)-1)):
                if (self.isAnyDuplicatedClassOnTheseFiles(listOfJars[i], listOfJars[j]) == True):
                    if (os.stat(listOfJars[i]).st_size >= os.stat(listOfJars[j]).st_size):
                        if (listOfJars[j] in bestJars):
                            bestJars.remove(listOfJars[j])
                        if ((listOfJars[i] in bestJars) == False and self.compareJarsWithJar(bestJars, listOfJars[i])):
                            bestJars.append(listOfJars[i])
                    elif (os.stat(listOfJars[j]).st_size >= os.stat(listOfJars[i]).st_size):
                        if (listOfJars[i] in bestJars):
                            bestJars.remove(listOfJars[i])
                        if ((listOfJars[j] in bestJars) == False and self.compareJarsWithJar(bestJars, listOfJars[j])):
                            bestJars.append(listOfJars[j])
                elif ((listOfJars[j] in bestJars) == False):
                        bestJars.append(listOfJars[j])


        if len(bestJars) > 0:
            return bestJars
        else:
            return listOfJars

    def compareJarsWithJar(self, allJars, jar):
        for oneJar in allJars:
            if (self.isAnyDuplicatedClassOnTheseFiles(oneJar, jar)):
                return False

        return True

    def isAnyDuplicatedClassOnTheseFiles(self, jarOne, jartwo):
        archive = zipfile.ZipFile(jarOne, 'r').namelist()
        archiveTwo = zipfile.ZipFile(jartwo, 'r').namelist()
        intersection_set = set.intersection(set(archive), set(archiveTwo))
        if (len(intersection_set)) > 0:
            return True
        else:
            return False