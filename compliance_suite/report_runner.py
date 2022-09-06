from report import Report, Phase, TestbedTest, Case
import json
import requests
from datetime import datetime
from generate_json import generate_report_json
from helper import Parser
import os


def report_runner(server_base_url, platform_name, platform_description, auth_type):
    # TODO: impelement bearer and passport, take the auth info from user
    if (auth_type == "no_auth"):
        auth = None
    elif (auth_type == "basic"):
        # auth = "Basic dXNlcm5hbWU6cGFzc3dvcmQ="
        auth = ("username", "password")
    elif (auth_type == "bearer"):
        auth = ""
    elif (auth_type == "passport"):
        auth = ""
    report_object = Report(
        schema_name = "ga4gh-testbed-report",
        schema_version = "0.1.0",
        testbed_name = "DRS Compliance Suite",
        testbed_version = "v0.0.0",
        testbed_description = "Test the compliance of a DRS implementation with GA4GH DRS v1.2.0 specification",
        platform_name = platform_name,
        platform_description = platform_description,
        input_parameters = {}
    )
    report_object.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    ##################################
    #### Phase: service-info......####
    ##################################
    service_info_phase = Phase("service info endpoint", "run all the tests for service_info endpoint")
    service_info_phase.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    service_info_test_1_obj = get_service_info_test(auth)
    service_info_phase.tests.append(service_info_test_1_obj)
    service_info_phase.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")



    ##################################
    #### Phase: service-info......####
    ##################################
    drs_object_phase = Phase("drs object info endpoint", "run all the tests for drs object info endpoint")
    drs_object_phase.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    # DRS_OBJECT_ID_1 = "697907bf-d5bd-433e-aac2-1747f1faf366" # present in the drs server
    DRS_OBJECT_ID_2 = "697907bf-d5bd-433e-aac2-1747f1faf377" # absent in the drs server
    # drs_object_1_obj = get_drs_object_test(auth, DRS_OBJECT_ID_1, expected_status_code="200")
    drs_object_2_obj = get_drs_object_test(auth, DRS_OBJECT_ID_2, expected_status_code="404")



    # drs_object_phase.tests.append(drs_object_1_obj)
    drs_object_phase.tests.append(drs_object_2_obj)
    drs_object_phase.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")






    report_object.phases.append(service_info_phase)
    report_object.phases.append(drs_object_phase)
    report_object.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    report_json = generate_report_json(report_object)
    return report_json

def get_service_info_test(auth):
    #### Service Info Test Cases ####
    #### 1. response status = 200 ####
    service_info_test_1_start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    SERVICE_INFO_URL = "/service-info"
    response = requests.request(method = "GET", url = server_base_url + SERVICE_INFO_URL, auth=auth)
    # check that response_status is 200 -> if no -> case fail, if yes -> case pass
    # if no -> check error response json valid or not
    # if yes -> check success response json valid or not

    # CASE: CHECK RESPONSE STATUS CODE
    case_validate_service_info_response_status = Case(
        case_name="service-info response status code validation",
        case_description="check if the response status code is 200",
        actual_response=response,
        response_schema_file = "",
        validate_schema = True,
        skip_case=False,
        skip_case_message=""
    )
    case_validate_service_info_response_status.validate_status_code("200")

    # CASE: CHECK RESPONSE CONTENT TYPE
    case_validate_service_info_response_content_type = Case(
        case_name="service-info response content-type validation",
        case_description="check if the content-type is application/json",
        actual_response=response,
        response_schema_file = "",
        validate_schema = True,
        skip_case=False,
        skip_case_message=""
    )
    case_validate_service_info_response_content_type.validate_content_type()

    skip_case_service_info_response = False
    skip_case_service_info_error = False
    skip_case_service_info_response_msg = ""
    skip_case_service_info_error_msg = ""

    if case_validate_service_info_response_status.status != "PASS" \
            or case_validate_service_info_response_content_type.status != "PASS":
        skip_case_service_info_response = True
        skip_case_service_info_response_msg = "skip validating service-info success response because status!=200 or content-type!=application/json"
    else:
        skip_case_service_info_error = True
        skip_case_service_info_error_msg = "skip validating service-info error response because status=200 and content-type=application/json"

    # CASE: CHECK SUCCESS RESPONSE SCHEMA
    case_validate_service_info_response_schema = Case(
        case_name="service-info success response schema validation",
        case_description="response status= 200",
        actual_response=response,
        response_schema_file = "service-info.json",
        validate_schema = True,
        skip_case=skip_case_service_info_response,
        skip_case_message=skip_case_service_info_response_msg
    )
    case_validate_service_info_response_schema.validate_response_schema()

    # CASE: CHECK ERROR RESPONSE SCHEMA
    case_validate_service_info_error_response_schema = Case(
        case_name="service-info error response schema validation",
        case_description="response status!= 200",
        actual_response=response,
        response_schema_file = "error.json",
        validate_schema = True,
        skip_case=skip_case_service_info_error,
        skip_case_message=skip_case_service_info_error_msg
    )
    case_validate_service_info_error_response_schema.validate_response_schema()

    service_info_test_name = "service-info"
    service_info_test_description = "validate service-info status code, content-type, response and error schemas"
    service_info_test_obj = TestbedTest(service_info_test_name,service_info_test_description)
    # Add cases to test object
    service_info_test_obj.cases = [
        case_validate_service_info_response_status,
        case_validate_service_info_response_content_type,
        case_validate_service_info_response_schema,
        case_validate_service_info_error_response_schema
    ]
    service_info_test_obj.start_time = service_info_test_1_start_time
    service_info_test_obj.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    return service_info_test_obj

def get_drs_object_test(auth, drs_object_id ,expected_status_code):
    #### DRS Object Test Cases ####
    #### 1. response status = 200 ####
    drs_object_test_start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    DRS_OBJECT_INFO_SUB_URL = "/objects/"
    response = requests.request(method = "GET", url = server_base_url + DRS_OBJECT_INFO_SUB_URL + drs_object_id, auth=auth)
    # check that response_status is 200 -> if no -> case fail, if yes -> case pass
    # if no -> check error response json valid or not
    # if yes -> check success response json valid or not

    # CASE: CHECK RESPONSE STATUS CODE
    case_validate_drs_object_response_status = Case(
        case_name="drs object response status code validation",
        case_description="check if the response status code = " + expected_status_code,
        actual_response=response,
        response_schema_file = "",
        validate_schema = True,
        skip_case=False,
        skip_case_message=""
    )
    case_validate_drs_object_response_status.validate_status_code(expected_status_code)

    # CASE: CHECK RESPONSE CONTENT TYPE
    case_validate_drs_object_response_content_type = Case(
        case_name="drs object response content-type validation",
        case_description="check if the content-type is application/json",
        actual_response=response,
        response_schema_file = "",
        validate_schema = True,
        skip_case=False,
        skip_case_message=""
    )
    case_validate_drs_object_response_content_type.validate_content_type()

    skip_case_drs_object_response = False
    skip_case_drs_object_error = False
    skip_case_drs_object_response_msg = ""
    skip_case_drs_object_error_msg = ""

    if (case_validate_drs_object_response_status.status != "PASS" \
            or case_validate_drs_object_response_content_type.status != "PASS") and expected_status_code == "200":
        skip_case_drs_object_response = True
        skip_case_drs_object_response_msg = "skip validating drs object success response because either" \
                                            "status!={} or content-type!=application/json".format(expected_status_code)
    else:
        skip_case_drs_object_error = True
        skip_case_drs_object_error_msg = "skip validating drs object error response because " \
                                         "status={} and content-type=application/json".format(expected_status_code)

    # CASE: CHECK SUCCESS RESPONSE SCHEMA
    case_validate_drs_object_response_schema = Case(
        case_name="drs object success response schema validation",
        case_description="response status= 200",
        actual_response=response,
        response_schema_file = "service-info.json",
        validate_schema = True,
        skip_case=skip_case_drs_object_response,
        skip_case_message=skip_case_drs_object_response_msg
    )
    case_validate_drs_object_response_schema.validate_response_schema()

    # CASE: CHECK ERROR RESPONSE SCHEMA
    case_validate_drs_object_error_response_schema = Case(
        case_name="drs object error response schema validation",
        case_description="response status!= 200",
        actual_response=response,
        response_schema_file = "error.json",
        validate_schema = True,
        skip_case=skip_case_drs_object_error,
        skip_case_message=skip_case_drs_object_error_msg
    )
    case_validate_drs_object_error_response_schema.validate_response_schema()

    drs_object_test_name = ("drs object for drs id: " + drs_object_id + ". drs object exists in the drs server") \
        if (expected_status_code == "200") else ("drs object for drs id: " + drs_object_id + ". drs object exists in the drs server")
    drs_object_test_description = "validate drs object status code, content-type, response and error schemas"
    drs_object_test_obj = TestbedTest(drs_object_test_name,drs_object_test_description)
    # Add cases to test object
    drs_object_test_obj.cases = [
        case_validate_drs_object_response_status,
        case_validate_drs_object_response_content_type,
        case_validate_drs_object_response_schema,
        case_validate_drs_object_error_response_schema

    ]
    drs_object_test_obj.start_time = drs_object_test_start_time
    drs_object_test_obj.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    return drs_object_test_obj







    # request_http_method = interaction["request"]["method"]
    # request_uri = server_base_url + interaction["request"]["uri"]
    # response = requests.request(method = request_http_method, url = request_uri, auth=auth)

    return








if __name__=="__main__":

    args = Parser.parse_args()
    server_base_url = args.server_base_url
    platform_name = args.platform_name
    platform_description = args.platform_description
    auth_type = args.auth_type

    output_report_file_path = "./output/report_"+datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%H-%M-%S")+".json"

    report_json = report_runner(server_base_url, platform_name, platform_description, auth_type);

    if not os.path.exists("./output"):
        os.makedirs("./output")

    # write output report to file
    with open(output_report_file_path, 'w', encoding='utf-8') as f:
        json.dump(report_json, f, ensure_ascii=False, indent=4)