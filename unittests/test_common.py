import os
import sys

# Append parent directory to import path to access methods under compliance_suite
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittests.utils import MockCase, MockResponse
from compliance_suite.cases.common import check_status_code, check_content_type

###

good_response = MockResponse({}) # Create empty response
good_response.headers = { "Content-Type": "application/json" }
good_response.status_code = 200

good_mock_case = MockCase(
    case_name = "good_response",
    actual_response = good_response
)

good_mock_case.expected_response = {
    "headers": { "Content-Type": "application/json" },
    "status": { "code": 200 }
}

###

bad_examples = [
    {
        "headers": {}, "status_code": 200
    },
    { 
        "headers": { "Content-Type": "application/json" }, "status_code": "none"
    },
    {
        "headers": { "Content-Type": "wrong" }, "status_code": 200
    },
    {
        "headers": { "Content-Type": "application/json" }, "status_code": 404
    }
]

bad_mock_cases = []

for i in range(len(bad_examples)):
    bad_response = MockResponse({}) # Create empty response
    bad_response.headers = bad_examples[i]["headers"]
    bad_response.status_code = bad_examples[i]["status_code"]

    bad_mock_case = MockCase(
        case_name = "bad_response_" + str(i),
        actual_response = bad_response
    )

    bad_mock_case.expected_response = {
        "headers": { "Content-Type": "application/json" },
        "status": { "code": 200 }
    }

    bad_mock_cases.append(bad_mock_case)

def test_status_code_unittest():
    good_mock_case.status = "NOT TESTED"
    check_status_code(good_mock_case)
    if good_mock_case.status != "PASS":
        return False
    
    # Has no status code
    check_status_code(bad_mock_cases[1])
    if bad_mock_cases[1].status != "FAIL":
        return False
    
    # Has status code 404
    check_status_code(bad_mock_cases[3])
    if bad_mock_cases[3].status != "FAIL":
        return False
    
    return True

def test_content_type_unittest():
    good_mock_case.status = "NOT TESTED"
    check_content_type(good_mock_case)
    if good_mock_case.status != "PASS":
        return False

    # Has no Content-Type
    bad_mock_cases[0].status = "NOT TESTED"
    check_content_type(bad_mock_cases[0])
    if bad_mock_cases[0].status != "FAIL":
        return False

    # Has wrong Content-Type
    bad_mock_cases[2].status = "NOT TESTED"
    check_content_type(bad_mock_cases[2])
    if bad_mock_cases[2].status != "FAIL":
        return False
    
    return True