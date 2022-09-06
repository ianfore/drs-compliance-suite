from datetime import datetime
import json
import jsonschema
from jsonschema import validate
import os

SCHEMA_FILE_PATH = "compliance_suite/schemas/"
SCHEMA_FILE_PATH_ABS = os.path.dirname(os.path.abspath(SCHEMA_FILE_PATH))

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
    def __init__(
            self,
            case_name,
            case_description,
            actual_response,
            response_schema_file = "",
            validate_schema = False,
            # expected_response,
            skip_case = False,
            skip_case_message = ""):
        self.case_name = case_name
        self.case_description = case_description
        self.start_time = ""
        self.end_time = ""
        self.status = "UNKNOWN"
        self.log_message = []
        self.message = ""
        self.response_schema_file = response_schema_file
        self.actual_response = actual_response
        self.validate_schema = validate_schema
        # self.expected_response = expected_response # TODO: Are we using expected_response?
        self.skip_case = skip_case
        self.skip_case_message = skip_case_message
        # self.run_case()

    def get_schema(self, schema_file_name):
        """This function loads the given schema available"""
        with open(schema_file_name, 'r') as file:
            schema = json.load(file)
        # TODO: throw exception -> fail case if schema file does not exist or add unittest to make sure all the schema files are available
        return schema

    def validate_response_schema(self):
        # import pdb; pdb.set_trace()
        self.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        if (self.skip_case == False):
            expected_schema_file_path = SCHEMA_FILE_PATH+ self.response_schema_file
            expected_schema = self.get_schema(expected_schema_file_path)
            abs_schema_file_path = os.path.dirname(os.path.abspath(expected_schema_file_path))
            reference_resolver = jsonschema.RefResolver(base_uri = "file://"+abs_schema_file_path+"/", referrer = None)
            # TODO: make sure actual_response is json -> if not error (FAIL)
            try:
                ### TODO: FIX!!!!! - Always passes!!!!!!!!!
                validate(instance = self.actual_response,resolver = reference_resolver,schema=expected_schema)
                self.message = "Schema Validation Successful"
                self.status = "PASS"
            except Exception as e:
                self.message = "Schema Validation Failed. " + e.message
                self.log_message.append("Stack Trace: "+str(e))
                self.status = "FAIL"
        else:
            self.status = "SKIP"
            self.message = self.skip_case_message
        self.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        return

    def validate_status_code(self, expected_status_code):
        self.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        if (self.skip_case == False):
            if str(self.actual_response.status_code) == expected_status_code:
                self.status = "PASS"
            else:
                self.status = "FAIL"
            self.message = "response status code = " + str(self.actual_response.status_code)
        else:
            self.status = "SKIP"
            self.message = self.skip_case_message
        self.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        return

    def validate_content_type(self):
        self.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        if (self.skip_case == False):
            if self.actual_response.headers["Content-Type"] == "application/json":
                self.status = "PASS"
                self.message = "content type = application/json"
            else:
                self.status = "FAIL"
                self.message = "content type = " + self.actual_response.headers["Content-Type"]
        else:
            self.status = "SKIP"
            self.message = self.skip_case_message
        self.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        return