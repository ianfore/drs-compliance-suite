from datetime import datetime

class Case():
    def __init__(self, case_name, case_description, algorithm, actual_response, expected_response):
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
        self.run_case()

    def run_case(self):
        self.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        self.algorithm(self)
        self.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")