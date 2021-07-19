import codecs
import os

from bs4 import BeautifulSoup

from nimrod.setup_tools.setup_tool import Setup_tool
from nimrod.tools.bin import JACOCOAGENT
from nimrod.tools.jacoco import Jacoco
from nimrod.tools.suite_generator import Suite


class Coverage_Report(Setup_tool):
    # scenario.merge_scenario.sut_class

    def generate_report(self, evo, scenario, commitMerge, toolOneSuites, toolTwoSuites, projectName):
        listaPacoteMetodoClasse = self.recuperaClassePacoteMetodo(scenario.merge_scenario.sut_method.replace("|", ","), scenario.merge_scenario.sut_class)

        listaPartesBasicasReport = ["target_commit", "test_suite_commit", "projeto"]
        listaCoberturaProjeto = ["randoop X: cobertura metodo SUA", "randoop Y: cobertura metodo SUA",
                                 "randoop X: cobertura classe SUA", "randoop Y: cobertura classe SUA",
                                 "randoop X: cobertura linha SUA", "randoop Y: cobertura linha SUA"]
        listaCoberturaClasse = ["classeTarget", "randoop X: cobertura metodo CUA", "randoop Y: cobertura metodo CUA",
                                "randoop X: cobertura linha CUA", "randoop Y: cobertura linha CUA"]
        listaCoberturaMetodo = ["Metodo Target", "randoop X: cobertura linha MUA", "randoop Y: cobertura linha MUA",
                                "randoop X: cobertura instruction MUA", "randoop Y: cobertura instruction MUA",
                                "randoop X: cobertura branch MUA", "randoop Y: cobertura branch MUA"]


        jacoco = Jacoco(java=evo.project_dep.java)

        try:
            for i in range(2):
                test_suite_tool_one = self.get_valid_test_suite(toolOneSuites, i*4, i*4+3)
                #dadosParaGravacaoRandoopX = self.retornaDadosParaAnalise(evo, toolOneSuites[0][2], toolOneSuites[0][7], jacoco,
                if (test_suite_tool_one != None):
                    #self.test_suite = self.get_new_suite(test_suite_tool_one[2], test_suite_tool_one[7])
                    if (isinstance(test_suite_tool_one, list)):
                        test_suite_commit = test_suite_tool_one[5]
                        test_suite_path_one = test_suite_tool_one[2]
                    else:
                        test_suite_path_one = test_suite_tool_one
                        test_suite_commit = commitMerge

                    dadosParaGravacaoRandoopX = self.retornaDadosParaAnalise(evo, test_suite_path_one, test_suite_commit, jacoco,
                                                                             scenario.merge_scenario.sut_class,
                                                                             listaPacoteMetodoClasse)
                    test_suite_tool_two = self.get_valid_test_suite(toolTwoSuites, i*4, i*4+3)
                    if (test_suite_tool_two != None):

                        if (isinstance(test_suite_tool_two, list)):
                            test_suite_commit = test_suite_tool_two[5]
                            test_suite_path_two = test_suite_tool_two[2]
                        else:
                            test_suite_path_two = test_suite_tool_two
                            test_suite_commit = commitMerge

                        #self.test_suite = self.get_new_suite(test_suite_tool_two[2], test_suite_tool_two[7])
                        dadosParaGravacaoRandoopY = self.retornaDadosParaAnalise(evo, test_suite_path_two, test_suite_commit, jacoco,
                                                                                 scenario.merge_scenario.sut_class,
                                                                                 listaPacoteMetodoClasse)

                        evo.output_coverage_metric.write_output_line(commitMerge, test_suite_commit, projectName, test_suite_path_one, test_suite_path_two, dadosParaGravacaoRandoopX, dadosParaGravacaoRandoopY, listaPartesBasicasReport,
                                              listaCoberturaProjeto, listaCoberturaClasse, listaCoberturaMetodo, scenario.merge_scenario.sut_class,
                                              listaPacoteMetodoClasse[0])

                if (isinstance(toolOneSuites, list) == False):
                    break;
        except Exception as e:
            print(e)

    def get_valid_test_suite(self, toolSuites, first_entry, last_entry):
        if(isinstance(toolSuites, list) == False):
            if (os.path.isdir(toolSuites+"/classes")):
                return toolSuites
        else:
            for i in range (first_entry, last_entry):
                if (len(toolSuites) > first_entry and toolSuites[i] != None and toolSuites[i][2] != None and os.path.isdir(toolSuites[i][2]+"/classes")):
                    return toolSuites[i]

        return None

    def retornaDadosParaAnalise(self, evo, path_suite, suite_merge, jacoco, classeTarget, listaPacoteMetodoClasse):
        global tagAClasseTarget
        global tagSpanMetodoTarget

        print("Classe Target ", classeTarget)

        listaJar = evo.project_dep.mergeDir.split(
            ":")  # Melhoria poderia ser feita removendo caractere do final da lista caso ele exista.
        listaJarInstrumentados = ""

        for j in range(len(listaJar) - 1):  # -1 pois existe um ultimo : ao final do evo.project_dep.classes_dir
            jacoco.execInstrumentJar(listaJar[j], path_suite)
            nomeJarInstrumentado = listaJar[j].split("/")  # recupera o nome do jar
            listaJarInstrumentados = listaJarInstrumentados + path_suite + "/" + nomeJarInstrumentado[len(
                nomeJarInstrumentado) - 1] + ":"  # nome do jar fica na ultima posicao da lista, : sao colocados para separar os jars

        listaJarInstrumentados = listaJarInstrumentados + JACOCOAGENT

        print("Iniciando execucao dos testes")
        #Instanciar um objeto aqui, e então realizar este run_test_suite
        #Importante mencionar, que seria necessário criar um objeto do tipo Suite...
        self.test_suite = self.get_new_suite(path_suite)

        self.run_test_suite(listaJarInstrumentados, evo.project_dep.sut_class, listaJarInstrumentados,
                            evo.project_dep)

        listaJar = list(filter(lambda x: x != '', listaJar))  # filtra registros vazios da lista

        print("Gerando report em html")
        jacoco.generateReportHtml(path_suite, listaJar, classeTarget)

        print("Gerando analise de todas classes do projeto")
        dadosReportProjeto = self.reportProjetoCompleto(path_suite)

        print("Gerando analise da classe target")
        dadosReportClasseTarget = self.reportClasseTarget(path_suite, listaPacoteMetodoClasse)

        print("Gerando analise do metodo target")
        if ("(" in listaPacoteMetodoClasse[0]) & (")" in listaPacoteMetodoClasse[0]):
            dadosReportMetodoTarget = self.reportMetodoTarget(path_suite, listaPacoteMetodoClasse)
        else:
            dadosReportMetodoTarget = [False]

        return [dadosReportProjeto, dadosReportClasseTarget, dadosReportMetodoTarget]

    # recupera pacote, nome da classe ou metodo target do teste
    def recuperaClassePacoteMetodo(self, pathMetodo, pathClasse):
        listaPacoteClasse = pathClasse.split(".")
        nomeClasse = listaPacoteClasse[len(listaPacoteClasse) - 1] # ultima posicao
        listaPacoteClasse.remove(nomeClasse)
        pacote = ".".join(listaPacoteClasse)
        nomeMetodo = pathMetodo[len(pathClasse) + 1:len(pathMetodo)]
        nomeMetodo = self.adjust_on_method_name(nomeMetodo)
        print("Metodo target: " + nomeMetodo)
        print("Classe target: " + nomeClasse)
        return [nomeMetodo, nomeClasse, pacote]

    # Ajusta nome do metodo removendo pacote do parametro dentro do metodo
    # Ex : getSchemaFromAnnotation(io.swagger.oas.annotations.media.Schema) ->  getSchemaFromAnnotation(Schema)
    def adjust_on_method_name(self, method_name):
        if ("(" in method_name) & (")" in method_name) & ("." in method_name):
            print("Required Adjust on Target Method Name")
            first_parenthesis = method_name.find("(")
            last_parenthesis = method_name.find(")")
            parameters = self.adjust_on_parameters(method_name[first_parenthesis:last_parenthesis])
            method_name = method_name[0:first_parenthesis + 1] + parameters + method_name[last_parenthesis] #")"# contatena por exemplo getSchemaFromAnnotation( + Schema)
        return method_name

    def adjust_on_parameters(self, parameters):
        parameters_list = parameters.split(",")
        adjusted_parameters = []
        for item in range (len(parameters_list)):
            if "." in parameters_list[item]:
                posicaoUltimoPonto = parameters_list[item].rindex(".")
                parameters_list[item] = parameters_list[item][posicaoUltimoPonto + 1:len(parameters_list[item])].replace("$", ".")
            else:
                parameters_list[item] = parameters_list[item][1:]
            adjusted_parameters.append(parameters_list[item])

        parameters = ""
        for item in range(len(adjusted_parameters)):
            parameters += adjusted_parameters[item]
            if (item < len(adjusted_parameters)-1):
                parameters += ", "

        return parameters

    def reportProjetoCompleto(self, path_suite):
        reportHtml = codecs.open(path_suite + "/report/index.html", 'r')

        soup = BeautifulSoup(reportHtml, 'html.parser')

        tagFoot = soup.find('tfoot')

        tagTr = list(tagFoot.children)[0]  # recupera a tag tr responsavel pela linha de resultados

        resultados = list(tagTr.children)

        totalClass = int((resultados[12].get_text()).replace(".", "").replace(",", ""))
        classesCobertas = int(totalClass - int((resultados[11].get_text()).replace(".", "").replace(",", "")))

        porcentagemCoberturaClasse = round((classesCobertas / totalClass) * 100, 2)

        totalMetodos = int((resultados[10].get_text()).replace(".", "").replace(",", ""))
        metodosCobertos = int(totalMetodos - int((resultados[9].get_text()).replace(".", "").replace(",", "")))

        porcentagemCoberturaMetodo = round((metodosCobertos / totalMetodos) * 100, 2)

        totalLinhas = int((resultados[8].get_text()).replace(".", "").replace(",", ""))
        linhasCobertas = int(totalLinhas - int((resultados[7].get_text()).replace(".", "").replace(",", "")))

        porcentagemCoberturaLinhas = round((linhasCobertas / totalLinhas) * 100, 2)

        return [porcentagemCoberturaClasse, porcentagemCoberturaMetodo, porcentagemCoberturaLinhas]

    def reportClasseTarget(self, path_suite, listaPacoteMetodoClasse):
        tagAClasseTarget = ''
        porcentagemCoberturaLinhasClasseTarget= ''
        porcentagemCoberturaMetodoClasseTarget = ''
        vaiGerarReportClasse = True

        reportClasseTarger = codecs.open(
            path_suite + "/report/" + listaPacoteMetodoClasse[2] + "/index.html",
            'r')  # abre o index.html relativo ao pacote da classe target

        soup = BeautifulSoup(reportClasseTarger, 'html.parser')

        tagsA = soup.find_all('a')  # recupera todas as tags a

        nomeClasseTarget = listaPacoteMetodoClasse[1]

        for i in range(len(tagsA)):
            if tagsA[i].get_text() == nomeClasseTarget:  # dentro das tags a escolhe a tag referente a classe target
                tagAClasseTarget = tagsA[i]
                break

        if tagAClasseTarget != '':
            tagTr = list(tagAClasseTarget.parents)[1]  # recupera a tag tr responsavel pela linha de resultados

            resultadosClasseTarget = list(tagTr.children)

            totalLinhasClasseTarget = int((resultadosClasseTarget[8].get_text()).replace(".", "").replace(",", ""))
            linhasCobertasClasseTarget = int(
                totalLinhasClasseTarget - int((resultadosClasseTarget[7].get_text()).replace(".", "").replace(",", "")))

            porcentagemCoberturaLinhasClasseTarget = round((linhasCobertasClasseTarget / totalLinhasClasseTarget) * 100,
                                                           2)

            totalMetodosClasseTarget = int((resultadosClasseTarget[10].get_text()).replace(".", "").replace(",", ""))
            metodosCobertosClasseTarget = int(
                totalMetodosClasseTarget - int((resultadosClasseTarget[9].get_text()).replace(".", "").replace(",", "")))

            porcentagemCoberturaMetodoClasseTarget = round(
                (metodosCobertosClasseTarget / totalMetodosClasseTarget) * 100,
                2)
        else:
            print("Classe target nao encontrado no projeto")
            vaiGerarReportClasse = False

        # Primeira posicao da lista indica se vai ser gerado um report com analise de classe target
        return [vaiGerarReportClasse, porcentagemCoberturaLinhasClasseTarget, porcentagemCoberturaMetodoClasseTarget]

    def reportMetodoTarget(self, path_suite, listaPacoteMetodoClasse):
        porcentagemBranchMetodoTarget = ''
        porcentagemInstrucMetodoTarget = ''
        tagSpanMetodoTarget = ''
        porcentagemCoberturaLinhasMetodoTarget = ''

        vaiGerarReportMetodo = True

        reportMetodoTarger = codecs.open(
            path_suite + "/report/" + listaPacoteMetodoClasse[2] + "/" + listaPacoteMetodoClasse[1] + ".html",
            'r')  # abre o html relativo a classe target

        soup = BeautifulSoup(reportMetodoTarger, 'html.parser')

        tagsSpam = soup.find_all('span')  # recupera todas as tags spam

        nomeMetodoTarget = listaPacoteMetodoClasse[0]

        for i in range(len(tagsSpam)):
            if tagsSpam[i].get_text() == nomeMetodoTarget:  # dentro das tags a escolhe a tag referente a classe target
                tagSpanMetodoTarget = tagsSpam[i]
                break
        if tagSpanMetodoTarget != '':
            tagTr = list(tagSpanMetodoTarget.parents)[1]

            resultadosMetodoTarget = list(tagTr.children)

            totalLinhasMetodoTarget = int((resultadosMetodoTarget[8].get_text()).replace(".", "").replace(",", ""))
            linhasCobertasMetodoTarget = int(
                totalLinhasMetodoTarget - int((resultadosMetodoTarget[7].get_text()).replace(".", "").replace(",", "")))

            porcentagemCoberturaLinhasMetodoTarget = round((linhasCobertasMetodoTarget / totalLinhasMetodoTarget) * 100,
                                                           2)
            print("Gerando analise instruct metodo target")
            porcentagemInstrucMetodoTarget = (resultadosMetodoTarget[2].get_text()).replace("%", "")

            print("Gerando analise branch metodo target")
            porcentagemBranchMetodoTarget = (resultadosMetodoTarget[4].get_text()).replace("%", "")
        else:
            print("Metodo target nao encontrado na classe target")
            vaiGerarReportMetodo = False

        # Primeira posicao da lista indica se vai ser gerado um report com analise de metodo target
        return [vaiGerarReportMetodo, porcentagemCoberturaLinhasMetodoTarget, porcentagemInstrucMetodoTarget,
                porcentagemBranchMetodoTarget]

    def get_new_suite(self, path_suite_dir):
        return Suite(suite_name=path_suite_dir, suite_dir=path_suite_dir,
                     suite_classes_dir=path_suite_dir+"/classes",
                     test_classes=['RegressionTest', 'ErrorTest'])

    def generate_test_suite(self, scenario, project_dep):
        print()