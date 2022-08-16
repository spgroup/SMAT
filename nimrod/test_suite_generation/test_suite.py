from typing import List


class TestSuite:
    def __init__(self, generator_name: str, commit: str, project: str, path: str, classPath: List[str]) -> None:
        self._generator_name = generator_name
        self._commit = commit
        self._project = project
        self._path = path
        self._classPath = classPath

    @property
    def generator_name(self) -> str:
        return self._generator_name

    @property
    def commit(self) -> str:
        return self._commit

    @property
    def project(self) -> str:
        return self._project

    @property
    def path(self) -> str:
        return self._path

    @property
    def classPath(self) -> List[str]:
        return self._classPath
