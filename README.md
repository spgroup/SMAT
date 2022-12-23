# SMAT: <i>Identifying Semantic Merge Conflicts Via Automated Behavior Change Detection</i>

This project aims to detect semantic conflicts by generating and running test suites on merge scenarios.

## Getting Started
- Clone the project locally using the command on your prompt: <i>git clone https://github.com/leusonmario/SMAT</i>
- After cloning, you must rename the configuration file <a href="https://github.com/leusonmario/SMAT/blob/master/nimrod/tests/env-config.template.json" target="_blank"><b>env-config.template.json</b></a> for <b>env-config.json</b>, and set up the required information for <b>java_home</b>. You must inform the location that Java was installed on your project. In case this environment variable is already configured, you don't need to inform this information again. For more information regarding the configuration, please refer to the [configuration documentation](docs/configuration.md).
- Next, you must inform the path of the file with the list of merge scenarios to be analyzed for the field <b>path_hash_csv</b>. Bellow, we provide further information to use the dataset we used to perform our study.
- Our scripts require Python 3.6.x. In case you are running the scripts on a Linux terminal, you can just call the semantic_study.py file (<b>python3 semantic_study.py</b>). As a result, the file <b>semantic_conflict_results.csv</b> and the folder <b>output-test-dest</b> grouping the generated test suites will be created.

## Getting Dataset
<ul>
  <li>Clone the project <a href="https://github.com/spgroup/mergedataset" target="_blank"><b>MergeDataSet</b></a> locally.</li>
  <li>Next, perform a checkout for the commit <a href="https://github.com/spgroup/mergedataset/commit/c8b965f71624f0ee3bec197d37ffbb2a9aaba97b" target="_blank">c8b965f</a>. </li>
  <li>Finally, run the script <a href="https://github.com/spgroup/mergedataset/blob/c8b965f71624f0ee3bec197d37ffbb2a9aaba97b/semantic-conflicts/get_sample.py" target="_blank">get_sample.py</a>. </li>
  <li>As a result, the file <b>results_semantic_study.csv</b> will be created. If you want to analyze other merge scenarios, you must provide a file the same information provided in our dataset.</li>
</ul>

## Providing input
SMAT allows the user to provide many scenarios for analysis using a JSON file. This JSON file consists of an array including each scenario that's going to be evaluated. The JSON file has the following structure:
```json
[
  {
    "projectName": "spring-boot",
    "runAnalysis": true,
    "scenarioCommits": {
      "base": "7578f2f824aac027529878810b76ee176b39e73a",
      "left": "0d00039ae7d01538de3f813b17d125dc5fdd5706",
      "right": "1c21f54bf91283d70e04c49ea09a4c05a885d7ac",
      "merge": "3eebbe1c8aed529e6903e78476492592ce0b0049"
    },
    "targets": {
      "org.springframework.boot.context.embedded.undertow.UndertowEmbeddedServletContainerFactory": [
        "createDeploymentManager(org.springframework.boot.context.embedded.ServletContextInitializer[])"
      ]
    },
    "scenarioJars": {
      "base": "/home/jpedroh/Projetos/cin/testes-smat/spring-boot/7578f2f824aac027529878810b76ee176b39e73a-createDeploymentManager.jar",
      "left": "/home/jpedroh/Projetos/cin/testes-smat/spring-boot/0d00039ae7d01538de3f813b17d125dc5fdd5706-createDeploymentManager.jar",
      "right": "/home/jpedroh/Projetos/cin/testes-smat/spring-boot/1c21f54bf91283d70e04c49ea09a4c05a885d7ac-createDeploymentManager.jar",
      "merge": "/home/jpedroh/Projetos/cin/testes-smat/spring-boot/3eebbe1c8aed529e6903e78476492592ce0b0049-createDeploymentManager.jar"
    },
    "jarType": "transformation"
  }
]
```
The scenarios file path can then be informed in the `env-config.json` file using the `input_path` field.

## Attentions When Using Windows
If you use Windows as your operating system, when you clone this project, you will probably receive an error message due to the size of a few file names. This problem will make it impossible for you to clone this repository.

To resolve this, you must install the Windows Subsystem for Linux (WSL); just follow the steps outlined in this [guide](https://docs.microsoft.com/pt-br/windows/wsl/install-win10). At the end of the installation, just open the Linux terminal on your Windows and clone the project as usual.

To execute the project, we advise you to use VSCode, because it has extensions to integrate with WSL. Once WSL is installed, when opening VSCode, a message will be displayed to download the Remote - WSL extension. With it, it is possible to edit all the files that are in WSL through VSCode and execute the project via terminal.
