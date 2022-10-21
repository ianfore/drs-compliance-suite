from ga4gh.testbed.report.status import Status
import json
import os
import jsonschema
from jsonschema import validate

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), 'schemas')

class ValidateResponse():
    def __init__(self):
        self.actual_response = ""
        self.expected_response = ""
        self.response_schema_file = ""
        self.case = ""

    def set_actual_response(self, actual_response):
        self.actual_response = actual_response

    def set_expected_response(self, expected_response):
        self.expected_response = expected_response

    def set_response_schema_file(self, response_schema_file):
        self.response_schema_file = response_schema_file

    def set_case(self, case):
        self.case = case

    def get_schema(self, schema_file_name):
        """This function loads the given schema available"""
        with open(schema_file_name, 'r') as file:
            schema = json.load(file)
        # TODO: throw exception -> fail case if schema file does not exist or add unittest to make sure all the schema files are available
        return schema

    def validate_response_schema(self):
        if self.case.get_status() != Status.SKIP:
            expected_schema_file_path = SCHEMA_DIR + "/" + self.response_schema_file
            expected_schema = self.get_schema(expected_schema_file_path)
            absolute_schema_file_path = os.path.dirname(os.path.abspath(expected_schema_file_path))
            reference_resolver = jsonschema.RefResolver(base_uri = "file://"+absolute_schema_file_path+"/", referrer = None)
            try:
                validate(instance = self.actual_response.json(),resolver = reference_resolver,schema=expected_schema)
                self.case.set_message("Schema Validation Successful")
                self.case.set_status_pass()
            except Exception as e:
                self.case.set_message(e.message if hasattr(e,"message") else str(e))
                self.case.add_log_message("Stack Trace: "+str(e))
                self.case.set_status_fail()
        else:
            pass
            # make sure if skip, the reason is added to message and/ log_message
        self.case.set_end_time_now()
        return

    def validate_status_code(self, expected_status_code):
        if self.case.get_status() != Status.SKIP:
            if str(self.actual_response.status_code) == expected_status_code:
                self.case.set_status_pass()
            else:
                self.case.set_status_fail()
            self.case.set_message("response status code = " + str(self.actual_response.status_code))
        else:
            # status = skip, message = reason
            pass
        self.case.set_end_time_now()
        return

    def validate_content_type(self, expected_content_type):
        if self.case.get_status() != Status.SKIP:
            if self.actual_response.headers["Content-Type"] == expected_content_type:
                self.case.set_status_pass()
                self.case.set_message("content type = " + expected_content_type)
            else:
                self.case.set_status_fail()
                self.case.set_message("content type = " + self.actual_response.headers["Content-Type"])
        else:
            pass
        self.case.set_end_time_now()
        return