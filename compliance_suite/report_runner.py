from ga4gh.testbed.report.report import Report
from validate_response import ValidateResponse
import json
import requests
from base64 import b64encode
from datetime import datetime
from compliance_suite.helper import Parser
import os
from compliance_suite.constants import *

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')

def report_runner(server_base_url, platform_name, platform_description, auth_type):

    # get authentication information from respective config file based on type of authentication
    is_passport_auth = False
    if (auth_type == "none"):
        headers = {}
        with open(CONFIG_DIR+"/config_"+auth_type+".json", 'r') as file:
            config = json.load(file)
    elif (auth_type == "basic"):
        with open(CONFIG_DIR+"/config_"+auth_type+".json", 'r') as file:
            config = json.load(file)
        username = config["username"]
        password = config["password"]
        b64_encoded_username_password = b64encode(str.encode("{}:{}".format(username, password))).decode("ascii")
        headers = { "Authorization" : "Basic {}".format(b64_encoded_username_password) }
    elif (auth_type == "bearer"):
        with open(CONFIG_DIR+"/config_"+auth_type+".json", 'r') as file:
            config = json.load(file)
        bearer_token = config["bearer_token"]
        headers =  { "Authorization" : "Bearer {}".format(bearer_token) }
    elif (auth_type == "passport"):
        with open(CONFIG_DIR+"/config_"+auth_type+".json", 'r') as file:
            config = json.load(file)
        headers = {}
        is_passport_auth = True
    drs_objects = config["drs_objects"]

    # Create a compliance report object
    report_object = Report()
    report_object.set_testbed_name(TESTBED_NAME)
    report_object.set_testbed_version(TESTBED_VERSION)
    report_object.set_testbed_description(TESTBED_DESCRIPTION)

    ### PHASE: /service-info
    service_info_phase = report_object.add_phase()
    service_info_phase.set_phase_name("service info endpoint")
    service_info_phase.set_phase_description("run all the tests for service_info endpoint")

    ### TEST: GET service-info
    service_info_test = service_info_phase.add_test()
    service_info_test.set_test_name("service-info")
    service_info_test.set_test_description("validate service-info status code, content-type, response and error schemas")

    SERVICE_INFO_URL = "/service-info"
    response = requests.request(method = "GET", url = server_base_url + SERVICE_INFO_URL, headers = headers)

    ### CASE: response status_code
    expected_status_code = "200"
    case_service_info_response_status = service_info_test.add_case()
    case_service_info_response_status.set_case_name("service-info response status code validation")
    case_service_info_response_status.set_case_description("check if the response status code is " + expected_status_code)

    validate_case_service_info_response_status = ValidateResponse()
    validate_case_service_info_response_status.set_case(case_service_info_response_status)
    validate_case_service_info_response_status.set_actual_response(response)
    validate_case_service_info_response_status.validate_status_code(expected_status_code)

    case_service_info_response_status.set_end_time_now()

    ### CASE: response content_type
    expected_content_type = "application/json"
    case_service_info_response_content_type = service_info_test.add_case()
    case_service_info_response_content_type.set_case_name("service-info response content-type validation")
    case_service_info_response_content_type.set_case_description("check if the content-type is " + expected_content_type)

    validate_case_service_info_response_content_type = ValidateResponse()
    validate_case_service_info_response_content_type.set_case(case_service_info_response_content_type)
    validate_case_service_info_response_content_type.set_actual_response(response)
    validate_case_service_info_response_content_type.validate_content_type(expected_content_type)

    case_service_info_response_content_type.set_end_time_now()

    ### CASE: response schema
    case_service_info_response_schema = service_info_test.add_case()
    case_service_info_response_schema.set_case_name("service-info success response schema validation")
    case_service_info_response_schema.set_case_description("validate service-info response schema when status = " + expected_status_code)

    validate_case_service_info_response_schema = ValidateResponse()
    validate_case_service_info_response_schema.set_case(case_service_info_response_schema)
    validate_case_service_info_response_schema.set_actual_response(response)
    validate_case_service_info_response_schema.set_response_schema_file(SERVICE_INFO_SCHEMA)
    validate_case_service_info_response_schema.validate_response_schema()

    case_service_info_response_schema.set_end_time_now()

    service_info_test.set_end_time_now()
    service_info_phase.set_end_time_now()

    ### PHASE: /object/{drs_id}

    drs_object_phase = report_object.add_phase()
    drs_object_phase.set_phase_name("drs object info endpoint")
    drs_object_phase.set_phase_description("run all the tests for drs object info endpoint")

    for this_drs_object in drs_objects:
        if this_drs_object["is_present_in_drs_server"]:
            expected_status_code = "200"
            expected_content_type = "application/json"
            test_description_substr = "present"
        # TODO: FIX THIS!!!
            schema_file = DRS_OBJECT_SCHEMA
        else:
            expected_status_code = "404"
            expected_content_type = "application/json"
            test_description_substr = "absent"
            schema_file = ERROR_SCHEMA
        this_drs_object_id = this_drs_object["id"]

        ### TEST: GET /objects/{this_drs_object_id}
        drs_object_test = drs_object_phase.add_test()
        drs_object_test.set_test_name("run test cases on the drs object info endpoint for drs id = "
                                      + this_drs_object["id"] + ". drs object is "
                                      + test_description_substr + " in the drs server")
        drs_object_test.set_test_description("validate drs object status code, content-type, response "
                                             "and error schemas when drs object is "
                                             + test_description_substr + " in the drs server",
                                             )

        this_drs_object_passport = None
        if is_passport_auth:
            this_drs_object_passport = this_drs_object["passport"]
            request_body = {"passports":[this_drs_object_passport]}
            response = requests.request(
                method = "POST",
                url = server_base_url + DRS_OBJECT_INFO_URL + this_drs_object_id,
                headers = headers,
                json = request_body)
        else:
            response = requests.request(method = "GET", url = server_base_url + DRS_OBJECT_INFO_URL + this_drs_object_id, headers = headers)

        ### CASE: response status_code
        case_drs_object_response_status = drs_object_test.add_case()
        case_drs_object_response_status.set_case_name("drs object response status code validation")
        case_drs_object_response_status.set_case_description("check if the response status code is " + expected_status_code)

        validate_case_drs_object_response_status = ValidateResponse()
        validate_case_drs_object_response_status.set_case(case_drs_object_response_status)
        validate_case_drs_object_response_status.set_actual_response(response)
        validate_case_drs_object_response_status.validate_status_code(expected_status_code)

        case_drs_object_response_status.set_end_time_now()

        ### CASE: response content_type
        case_drs_object_response_content_type = drs_object_test.add_case()
        case_drs_object_response_content_type.set_case_name("drs object response content-type validation")
        case_drs_object_response_content_type.set_case_description("check if the content-type is " + expected_content_type)

        validate_drs_object_info_response_content_type = ValidateResponse()
        validate_drs_object_info_response_content_type.set_case(case_drs_object_response_content_type)
        validate_drs_object_info_response_content_type.set_actual_response(response)
        validate_drs_object_info_response_content_type.validate_content_type(expected_content_type)

        case_drs_object_response_content_type.set_end_time_now()

        ### CASE: response schema

        case_drs_object_response_schema = drs_object_test.add_case()
        case_drs_object_response_schema.set_case_name("drs object response schema validation")
        case_drs_object_response_schema.set_case_description("validate drs object response schema when status = " + expected_status_code)

        validate_case_drs_object_response_schema = ValidateResponse()
        validate_case_drs_object_response_schema.set_case(case_drs_object_response_schema)
        validate_case_drs_object_response_schema.set_actual_response(response)
        if this_drs_object["is_present_in_drs_server"]:
            validate_case_drs_object_response_schema.set_response_schema_file(DRS_OBJECT_SCHEMA)
        else:
            validate_case_drs_object_response_schema.set_response_schema_file(ERROR_SCHEMA)
        validate_case_drs_object_response_schema.validate_response_schema()

        case_drs_object_response_schema.set_end_time_now()

        drs_object_test.set_end_time_now()
        drs_object_phase.set_end_time_now()
    report_object.set_end_time_now()
    report_object.finalize()
    return report_object.to_json()

def main():
    args = Parser.parse_args()
    output_report_file_path = "./output/report_"+datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%H-%M-%S")+".json"

    output_report = report_runner(server_base_url = args.server_base_url,
                                platform_name = args.platform_name,
                                platform_description = args.platform_description,
                                auth_type = args.auth_type)

    output_report_json = json.loads(output_report)

    if not os.path.exists("./output"):
        os.makedirs("./output")

    # write output report to file
    with open(output_report_file_path, 'w', encoding='utf-8') as f:
        json.dump(output_report_json, f, ensure_ascii=False, indent=4)

if __name__=="__main__":
    main()