from compliance_suite.report import Report, Phase, TestbedTest, Case
import requests

good_mock_server_no_auth = "http://localhost:8086/ga4gh/drs/v1"
good_mock_server_basic = "http://localhost:8087/ga4gh/drs/v1"
good_mock_server_bearer = "http://localhost:8088/ga4gh/drs/v1"
good_mock_server_passport = "http://localhost:8089/ga4gh/drs/v1"
SERVICE_INFO_URL = "/service-info"

def test_case_service_info_response_status():
    headers = {}
    response = requests.request(method = "GET", url =good_mock_server_no_auth + SERVICE_INFO_URL, headers ={})
    expected_status_code = "200"
    case_validate_service_info_response_status = Case(
        case_name="service-info response status code validation",
        case_description="check if the response status code is 200",
        actual_response=response
    )
    case_validate_service_info_response_status.validate_status_code(expected_status_code)
    assert case_validate_service_info_response_status.status == "PASS"

def test_case_service_info_response_content_type():
    headers = {}
    response = requests.request(method = "GET", url =good_mock_server_no_auth + SERVICE_INFO_URL, headers ={})
    expected_content_type = "application/json"
    case_validate_service_info_response_content_type = Case(
        case_name="service-info response content-type validation",
        case_description="check if the content-type is " + expected_content_type,
        actual_response=response
    )
    case_validate_service_info_response_content_type.validate_content_type(expected_content_type)
    assert case_validate_service_info_response_content_type.status == "PASS"