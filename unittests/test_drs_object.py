import os
import sys

# Append parent directory to import path to access methods under compliance_suite
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittests.utils import MockCase, MockResponse
from unittests.resources.expected_drs_objects import expected_good_drs_object
from unittests.resources.expected_drs_objects import expected_bad_drs_objects
from compliance_suite.cases.drs_object import check_required_drs_object_info_attr

###

good_drs_obj_response = MockResponse(
    response = expected_good_drs_object
)

good_mock_case = MockCase(
    case_name = "good_drs_obj",
    actual_response = good_drs_obj_response
)

###

bad_mock_cases = []

for i in range(len(expected_bad_drs_objects)):
    bad_drs_obj_response = MockResponse(
        response = expected_bad_drs_objects[i]
    )

    bad_mock_case = MockCase(
        case_name = "bad_drs_obj_" + str(i),
        actual_response = bad_drs_obj_response
    )

    bad_mock_cases.append(bad_mock_case)
    
###

def test_check_required_drs_object_info_attr_good_mock_case():
    check_required_drs_object_info_attr(good_mock_case)
    assert good_mock_case.status == "PASS"

def test_check_required_drs_object_info_attr_bad_mock_case():
    for bad_mock_case in bad_mock_cases:
        check_required_drs_object_info_attr(bad_mock_case)
        assert bad_mock_case.status == "FAIL"