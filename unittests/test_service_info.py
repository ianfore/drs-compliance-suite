import os
import sys
import pytest

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

def test_service_info_attr_good_mock_case():
    check_required_service_info_attr(good_mock_case)
    assert good_mock_case.status == "PASS"

def test_service_info_attr_bad_mock_case():
    check_required_service_info_attr(bad_mock_case)
    assert bad_mock_case.status == "FAIL"

def test_service_info_type_attr_good_mock_case():
    check_required_service_info_type_attr(good_mock_case)
    assert good_mock_case.status == "PASS"

def test_service_info_type_attr_bad_mock_case():
    check_required_service_info_type_attr(bad_mock_case)
    assert bad_mock_case.status == "FAIL"

def test_service_info_org_attr_good_mock_case():
    check_required_service_info_org_attr(good_mock_case)
    assert good_mock_case.status == "PASS"

def test_service_info_org_attr_bad_mock_case():
    check_required_service_info_org_attr(bad_mock_case)
    assert bad_mock_case.status == "FAIL"