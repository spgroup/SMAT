import unittest
from unittest import TestCase

from nimrod.tests.utils import get_config
from nimrod.tools.java import Java
from nimrod.tools.jacoco import Jacoco
from nimrod.report_metrics.coverage.coverage_report import Coverage_Report


class TestJacoco(TestCase):

    @classmethod
    def setUp(cls):
        cls.java_home = get_config()['java_home']
        cls.java = Java(cls.java_home)
        cls.jacoco = Jacoco(cls.java)

    # Teste do comando java -jar jacococli.jar instrument "jar_a_ser_modificado" --dest "local_jar_instrumentado"
    @unittest.skip("invalid inputs")
    def test_instrument(self):

        jarSemModificacaoes = "/home/vinicius/Documentos/UFPE/TCC/mergedataset/cloud-slang/20bac30d9bd76569aa6a4fa1e8261c1a9b5e6f76/original/base/cloudslang-all-0.7.50-SNAPSHOT-jar-with-dependencies.jar"
        destinoJarInstrumentado = "/home/vinicius/Documentos/UFPE/TCC/Resultados/CloudSlang/cloudslang-all/dest"

        self.jacoco.execInstrumentJar(jarSemModificacaoes, destinoJarInstrumentado)

    @unittest.skip("invalid inputs")
    def test_runTest(self):

        projectJar = "/home/vinicius/Documentos/UFPE/TCC/Resultados/CloudSlang/cloudslang-all/dest/cloudslang-all-0.7.50-SNAPSHOT-jar-with-dependencies.jar"
        suiteClass = "/home/vinicius/Documentos/UFPE/TCC/Resultados/CloudSlang/cloudslang-all/Class/"
        test_class = "RegressionTest0"

        self.jacoco.createJacocoExec(projectJar, suiteClass, test_class)

    @unittest.skip("invalid inputs")
    def test_generateReport(self):
        jacocoExecDir = "/home/vinicius/Documentos/UFPE/TCC/SMAT/nimrod/tests/tools/jacoco.exec"
        classFile = "/home/vinicius/Documentos/UFPE/TCC/Projetos/cloud-slang/cloudslang-all/target/classes/io/cloudslang/lang/api"
        csvFile = "/home/vinicius/Documentos/UFPE/TCC/Resultados/CloudSlang/cloudslang-all/dest/report.csv"

        self.jacoco.generateReport(jacocoExecDir, classFile, csvFile)

    def test_method_adjust_without_primitive_types(self):
        coverage_report = Coverage_Report()
        self.assertEqual("outerHtmlHead(StringBuilder, OutputSettings)", coverage_report.adjust_on_method_name("outerHtmlHead(java.lang.StringBuilder, org.jsoup.nodes.OutputSettings)"))

    def test_method_adjust_with_inner_class_types(self):
        coverage_report = Coverage_Report()
        self.assertEqual("outerHtmlHead(StringBuilder, int, Document.OutputSettings)", coverage_report.adjust_on_method_name("outerHtmlHead(java.lang.StringBuilder, int, org.jsoup.nodes.Document$OutputSettings)"))

    def test_method_adjust_with_primitive_types(self):
        coverage_report = Coverage_Report()
        self.assertEqual("outerHtmlHead(StringBuilder, int, String, OutputSettings)", coverage_report.adjust_on_method_name("outerHtmlHead(java.lang.StringBuilder, int, String, org.jsoup.nodes.OutputSettings)"))