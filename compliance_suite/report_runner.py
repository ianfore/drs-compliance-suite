from report import Report, Phase, TestbedTest, Case
from cases.service_info import check_required_service_info_attr, check_required_service_info_type_attr, check_required_service_info_org_attr
from cases.common import check_status_code, check_content_type
from cases.drs_object import check_all_drs_object_info_attr, check_all_drs_object_info_attr_types, \
    check_required_drs_object_info_attr, check_required_drs_object_info_checksums_attr, \
    check_drs_object_info_access_methods_attr
import json
import requests
from generate_json import generate_report_json
from datetime import datetime
from helper import Parser
import os

def report_runner(server_base_url, platform_name, platform_description, auth_type):
    # TODO: impelement bearer and passport, take the auth info from user
    if (auth_type == "no_auth"):
        auth = None
    elif (auth_type == "basic"):
        # auth = "Basic dXNlcm5hbWU6cGFzc3dvcmQ="
        auth = ("username", "password");
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

    interactions_file_path="./compliance_suite/interactions/"
    with open(interactions_file_path+"service_info.json") as f:
        service_info_interactions = json.load(f)

    service_info_phase = Phase(service_info_interactions["phase_name"], service_info_interactions["phase_description"])
    service_info_phase.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    # for each interaction, send the request and verify if the response is as expected
    for interaction in service_info_interactions["interactions"]:
        this_test_start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        request_http_method = interaction["request"]["method"]
        request_uri = server_base_url + interaction["request"]["uri"]
        response = requests.request(method = request_http_method, url = request_uri, auth=auth)
        skip_case = False
        skip_case_message = ""
        case_status_code = Case(
            case_name="status_code",
            case_description="check if the service-info response is as expected",
            algorithm=check_status_code,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        # if expected_status != 200, skip the rest of the tests
        if interaction["response"]["status"]["code"]!=200:
            skip_case = True
            skip_case_message = "Skipping this case as we are testing a failure condition. Expected response status_code = {}"

        if case_status_code.status == "FAIL":
            skip_case = True
            skip_case_message = "Skipping this case as response status is not as expected"

        case_content_type = Case(
            case_name="content-type",
            case_description="check if the response Content-Type is as expected",
            algorithm=check_content_type,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        case_required_service_info_attr = Case(
            case_name="required response fields",
            case_description="check if the response contains all the required attributes",
            algorithm=check_required_service_info_attr,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        case_required_service_info_type_attr = Case(
            case_name="required response service type fields",
            case_description="check if the response 'type' field contains all the required attributes",
            algorithm=check_required_service_info_type_attr,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        case_required_service_info_org_attr = Case(
            case_name="required response service type fields",
            case_description="check if the response 'type' field contains all the required attributes",
            algorithm=check_required_service_info_org_attr,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        this_test_name = interaction["test_name"]
        this_test_description = interaction["test_description"]
        this_test_obj = TestbedTest(this_test_name,this_test_description)
        this_test_obj.cases = [
            case_status_code,
            case_content_type,
            case_required_service_info_attr,
            case_required_service_info_type_attr,
            case_required_service_info_org_attr
        ]
        this_test_obj.start_time = this_test_start_time
        this_test_obj.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        service_info_phase.tests.append(this_test_obj)

    service_info_phase.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    report_object.phases.append(service_info_phase)

    with open(interactions_file_path+"drs_object.json") as f:
        drs_object_interactions = json.load(f)

    drs_object_phase = Phase(drs_object_interactions["phase_name"], drs_object_interactions["phase_description"])
    drs_object_phase.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")


    # for each interaction, send the request and verify if the response is as expected
    for interaction in drs_object_interactions["interactions"]:
        this_test_start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        request_http_method = interaction["request"]["method"]
        request_uri = server_base_url + interaction["request"]["uri"]
        response = requests.request(method = request_http_method, url = request_uri, auth=auth)
        skip_case = False
        skip_case_message = ""
        case_status_code = Case(
            case_name="status_code",
            case_description="check if the drs object info response is as expected",
            algorithm=check_status_code,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        # if expected_status != 200, skip the rest of the tests
        if interaction["response"]["status"]["code"]!=200:
            skip_case = True
            skip_case_message = "Skipping this case as we are testing a failure condition. Expected response status_code = {}"

        if case_status_code.status == "FAIL":
            skip_case = True
            skip_case_message = "Skipping this case as response status is not as expected"

        case_content_type = Case(
            case_name="content-type",
            case_description="check if the response Content-Type is as expected",
            algorithm=check_content_type,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        case_all_drs_object_info_attr = Case(
            case_name="all fields in drs object info response",
            case_description="check if there are undefined attributes present in the drs object info response",
            algorithm=check_all_drs_object_info_attr,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        # import pdb;pdb.set_trace()

        case_all_drs_object_info_attr_types = Case(
            case_name="data types of all fields in drs object info response",
            case_description="check if all the attributes in drs object info response have expected data types",
            algorithm=check_all_drs_object_info_attr_types,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        case_required_drs_object_info_attr = Case(
            case_name="required fields in drs object info response",
            case_description="check if the response contains all the required attributes",
            algorithm=check_required_drs_object_info_attr,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        case_required_drs_object_info_checksums_attr = Case(
            case_name="required response checksums fields",
            case_description="check if the response 'checksums' field contains all the required attributes",
            algorithm=check_required_drs_object_info_checksums_attr,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        case_drs_object_info_access_methods_attr = Case(
            case_name="access_methods field in drs object info response",
            case_description="check if access_methods is a list of access_method objects",
            algorithm=check_drs_object_info_access_methods_attr,
            actual_response=response,
            expected_response= interaction["response"],
            skip_case=skip_case,
            skip_case_message=skip_case_message
        )

        this_test_name = interaction["test_name"]
        this_test_description = interaction["test_description"]
        this_test_obj = TestbedTest(this_test_name,this_test_description)
        this_test_obj.start_time = this_test_start_time
        this_test_obj.cases = [
            case_status_code,
            case_content_type,
            case_all_drs_object_info_attr,
            case_all_drs_object_info_attr_types,
            case_required_drs_object_info_attr,
            case_required_drs_object_info_checksums_attr,
            case_drs_object_info_access_methods_attr
        ]
        this_test_obj.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        drs_object_phase.tests.append(this_test_obj)
        # TODO: update - this_test_obj.summary

    drs_object_phase.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    report_object.phases.append(drs_object_phase)
    report_object.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    report_json = generate_report_json(report_object)
    return report_json

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