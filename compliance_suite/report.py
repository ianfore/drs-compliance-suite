from datetime import datetime

class Report():
    def __init__(
            self,
            schema_name,
            schema_version,
            testbed_name,
            testbed_version,
            testbed_description,
            platform_name,
            platform_description,
            input_parameters
    ):
        self.schema_name = schema_name # "ga4gh-testbed-report"
        self.schema_version = schema_version # "0.1.0"
        self.testbed_name = testbed_name
        self.testbed_version = testbed_version
        self.testbed_description = testbed_description
        self.platform_name = platform_name
        self.platform_description = platform_description
        self.input_parameters = input_parameters # or update with input params?
        self.start_time = ""
        self.end_time = ""
        self.status = ""
        self.summary = {
            "unknown": 0,
            "passed":0,
            "warned":0,
            "failed":0,
            "skipped":0
        }
        self.message = ""
        self.phases = []

class Phase():
    def __init__(self, phase_name, phase_description):
        self.phase_name = phase_name
        self.phase_description = phase_description
        self.start_time = ""
        self.end_time = ""
        self.status = ""
        self.summary = {
            "unknown": 0,
            "passed":0,
            "warned":0,
            "failed":0,
            "skipped":0
        }
        self.tests = []

class TestbedTest():
    def __init__(self, test_name, test_description):
        self.test_name = test_name
        self.test_description = test_description
        self.start_time = ""
        self.end_time = ""
        self.status = ""
        self.summary = {
            "unknown": 0,
            "passed":0,
            "warned":0,
            "failed":0,
            "skipped":0
        }
        self.message = ""
        self.cases = []

class Case():
    # TODO: Add skip field, when skip is set, the case is not applicable for a given test interaction and will be skipped
    def __init__(self, case_name, case_description, algorithm, actual_response, expected_response, skip_case = False, skip_case_message = ""):
        self.case_name = case_name
        self.case_description = case_description
        self.start_time = ""
        self.end_time = ""
        self.status = ""
        self.log_message = []
        self.message = ""
        self.algorithm = algorithm
        self.actual_response = actual_response
        self.expected_response = expected_response
        self.skip_case = skip_case
        self.skip_case_message = skip_case_message
        self.run_case()

    def run_case(self):
        self.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        if (self.skip_case == False):
            self.algorithm(self)
        else:
            self.status = "SKIP"
            self.message = self.skip_case_message
        self.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")