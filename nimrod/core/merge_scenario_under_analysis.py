from typing import List, Dict


class MergeScenarioUnderAnalysis:
    def __init__(self, project_name: str, run_analysis: bool, scenario_commits: "ScenarioInformation", targets: "Dict[str, List[str]]", scenario_jars: "ScenarioInformation", jar_type: str):
        self.project_name = project_name
        self.run_analysis = run_analysis
        self.scenario_commits = scenario_commits
        self.targets = targets
        self.scenario_jars = scenario_jars
        self.jar_type = jar_type


class ScenarioInformation:
    def __init__(self, base: str, left: str, right: str, merge: str):
        self.base = base
        self.left = left
        self.right = right
        self.merge = merge
