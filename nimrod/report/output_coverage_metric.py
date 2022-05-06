import os
from nimrod.report.output import Output

class Output_coverage_metric(Output):

    def get_file_collumn_names(self):
        listaPartesBasicasReport = ["target_commit", "test_suite_commit", "project_name", "path_suite_one", "path_suite_two"]
        listaCoberturaProjeto = ["randoop X: method coverage SUA", "randoop Y: method coverage SUA",
                                 "randoop X: class coverage SUA", "randoop Y: class coverage SUA",
                                 "randoop X: line coverage SUA", "randoop Y: line coverage SUA"]
        listaCoberturaClasse = ["target_class", "randoop X: method coverage CUA", "randoop Y: method coverage CUA",
                                "randoop X: line coverage CUA", "randoop Y: line coverage CUA"]
        listaCoberturaMetodo = ["target_method", "randoop X: cobertura linha MUA", "randoop Y: cobertura linha MUA",
                                "randoop X: instruction coverage MUA", "randoop Y: instruction coverage MUA",
                                "randoop X: branch coverage MUA", "randoop Y: branch coverage MUA"]
        listaJarType=["jar_type"]

        return listaPartesBasicasReport + listaCoberturaProjeto + listaCoberturaClasse + listaCoberturaMetodo + listaJarType

    def write_output_line(self, commitVersion, test_suite_commit, projectName, path_suite_one, path_suite_two, dadosParaGravacaoRandoopX, dadosParaGravacaoRandoopY, listaPartesBasicasReport,
                          listaCoberturaProjeto, listaCoberturaClasse, listaCoberturaMetodo, classeTarget, nomeMetodoTarget, jar_type=None):
        if (os.path.isfile(self.output_file_path) == False):
            self.create_result_file()
        else:
            self.write_each_result(self.formate_output_line(commitVersion, test_suite_commit, projectName, path_suite_one, path_suite_two, dadosParaGravacaoRandoopX, dadosParaGravacaoRandoopY, listaPartesBasicasReport,
                                                            listaCoberturaProjeto, listaCoberturaClasse, listaCoberturaMetodo, classeTarget.replace(",","|"), nomeMetodoTarget.replace(",","|"), jar_type))

    def formate_output_line(self, commitVersion, test_suite_commit, projectName, path_suite_one, path_suite_two, dadosParaGravacaoRandoopX, dadosParaGravacaoRandoopY, listaPartesBasicasReport,
                            listaCoberturaProjeto, listaCoberturaClasse, listaCoberturaMetodo, classeTarget, nomeMetodoTarget, jar_type=None):
        try:
            if (dadosParaGravacaoRandoopX[1][0] is True) & (dadosParaGravacaoRandoopY[1][0] is True): # se possuir classe target
                if (dadosParaGravacaoRandoopX[2][0] is True) & (dadosParaGravacaoRandoopY[2][0] is True): # se possuir metodo target
                    return [commitVersion, test_suite_commit, projectName, path_suite_one, path_suite_two, dadosParaGravacaoRandoopX[0][1], dadosParaGravacaoRandoopY[0][1],
                                     dadosParaGravacaoRandoopX[0][0], dadosParaGravacaoRandoopY[0][0], dadosParaGravacaoRandoopX[0][2],
                                     dadosParaGravacaoRandoopY[0][2], classeTarget, dadosParaGravacaoRandoopX[1][2],
                                     dadosParaGravacaoRandoopY[1][2], dadosParaGravacaoRandoopX[1][1], dadosParaGravacaoRandoopY[1][1],
                                     nomeMetodoTarget, dadosParaGravacaoRandoopX[2][1], dadosParaGravacaoRandoopY[2][1],
                                     dadosParaGravacaoRandoopX[2][2], dadosParaGravacaoRandoopY[2][2], dadosParaGravacaoRandoopX[2][3],
                                     dadosParaGravacaoRandoopY[2][3], jar_type]
                else:
                   return [commitVersion, test_suite_commit, projectName, path_suite_one, path_suite_two, dadosParaGravacaoRandoopX[0][1], dadosParaGravacaoRandoopY[0][1],
                                     dadosParaGravacaoRandoopX[0][0], dadosParaGravacaoRandoopY[0][0], dadosParaGravacaoRandoopX[0][2],
                                     dadosParaGravacaoRandoopY[0][2], classeTarget, dadosParaGravacaoRandoopX[1][2],
                                     dadosParaGravacaoRandoopY[1][2], dadosParaGravacaoRandoopX[1][1], dadosParaGravacaoRandoopY[1][1],
                                     "", "", "",
                                     "", "", "",
                                     "", jar_type]
            else:
                return [commitVersion, test_suite_commit, path_suite_one, path_suite_two, projectName, dadosParaGravacaoRandoopX[0][1], dadosParaGravacaoRandoopY[0][1],
                        dadosParaGravacaoRandoopX[0][0], dadosParaGravacaoRandoopY[0][0], dadosParaGravacaoRandoopX[0][2],
                        dadosParaGravacaoRandoopY[0][2], "", "",
                        "", "", "",
                        "", "", "",
                        "", "", "",
                        "", jar_type]
        except Exception as e:
            print(e)
        return [commitVersion, "", projectName, "", "", "","","","","","","","","","","","","","","","","","", jar_type]