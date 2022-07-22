class Test():
    def __init__(self, test_name, test_description):
        self.test_name = test_name
        self.case_description = test_description
        self.start_time = ""
        self.end_time = ""
        self.status = ""
        self.log_message = []
        self.message = ""
        self.cases = []