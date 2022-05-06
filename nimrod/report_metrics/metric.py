from abc import abstractmethod

class Metric:
    @abstractmethod
    def metrics_comparison(self, path_suite_original, path_suite_modified) -> dict:
        pass

    @abstractmethod
    def extract_data(self, data, report_path, randoop_original_report) -> dict:
        pass
