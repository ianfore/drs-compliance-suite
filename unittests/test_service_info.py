import os
import sys

# Append parent directory to import path to access methods under compliance_suite
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittests.utils import MockCase, MockResponse
from unittests.resources.expected_service_info import expected_good_service_info_response
from unittests.resources.expected_service_info import expected_bad_service_info_response
from compliance_suite.cases.service_info import check_required_service_info_attr, check_required_service_info_type_attr, check_required_service_info_org_attr

###

good_mock_response = MockResponse(
    response = expected_good_service_info_response
)

good_mock_case = MockCase(
    case_name = "good_mock_case",
    actual_response = good_mock_response
)

###

bad_mock_response = MockResponse(
    response = expected_bad_service_info_response
)

bad_mock_case = MockCase(
    case_name = "bad_mock_case",
    actual_response = bad_mock_response
)

###

service_info_methods = [
    check_required_service_info_attr, 
    check_required_service_info_type_attr, 
    check_required_service_info_org_attr
]

mock_cases = [ 
    { "case": good_mock_case, "expected_response": "PASS" },
    { "case": bad_mock_case, "expected_response": "FAIL" }
]

# Should this be named something else?
def test_service_info_unittest():
    for method in service_info_methods:
        for mock_case in mock_cases:
            method(mock_case["case"])
            if mock_case["case"].status != mock_case["expected_response"]:
                return False

    return True