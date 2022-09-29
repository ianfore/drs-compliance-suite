from compliance_suite.report import Report, Phase, TestbedTest, Case
import requests
from unittests.constants import SERVICE_INFO_URL, GOOD_MOCK_SERVER_NO_AUTH, GOOD_MOCK_SERVER_BASIC, GOOD_MOCK_SERVER_BEARER, GOOD_MOCK_SERVER_PASSPORT
from base64 import b64encode
import pytest
from compliance_suite.constants import SCHEMA_SERVICE_INFO


def get_auth_type_data_provider():
    headers_no_auth = {}
    b64_encoded_username_password = b64encode(str.encode("{}:{}".format("username", "password"))).decode("ascii")
    headers_basic = { "Authorization" : "Basic {}".format(b64_encoded_username_password) }
    headers_bearer =  { "Authorization" : "Bearer {}".format("secret-token-1") }
    auth_type_data_provider = [
        ("GET", headers_basic, GOOD_MOCK_SERVER_BASIC ,"basic"),
        ("GET", headers_no_auth, GOOD_MOCK_SERVER_NO_AUTH ,"no_auth" ),
        ("GET", headers_bearer, GOOD_MOCK_SERVER_BEARER, "bearer")
    ]
    return auth_type_data_provider

@pytest.mark.parametrize("headers, server_base_url, auth_type", get_auth_type_data_provider())
def test_case_service_info(headers, server_base_url, auth_type):
    response = requests.request(method = "GET", url =server_base_url + SERVICE_INFO_URL, headers = headers)
    expected_status_code = "200"
    case_validate_service_info_response_status = Case(
        case_name="service-info response status code validation",
        case_description="check if the response status code is 200",
        actual_response=response
    )
    case_validate_service_info_response_status.validate_status_code(expected_status_code)
    assert case_validate_service_info_response_status.status == "PASS"

    expected_content_type = "application/json"
    case_validate_service_info_response_content_type = Case(
        case_name="service-info response content-type validation",
        case_description="check if the content-type is " + expected_content_type,
        actual_response=response
    )
    case_validate_service_info_response_content_type.validate_content_type(expected_content_type)
    assert case_validate_service_info_response_content_type.status == "PASS"

    case_validate_service_info_response_schema = Case(
        case_name="service-info success response schema validation",
        case_description="validate service-info response schema when status= 200",
        actual_response=response,
        response_schema_file = SCHEMA_SERVICE_INFO,
        skip_case=False,
        skip_case_message=""
    )
    case_validate_service_info_response_schema.validate_response_schema()
    assert case_validate_service_info_response_content_type.status == "PASS"