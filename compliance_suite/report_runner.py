from ga4gh.testbed.report.report import Report
from compliance_suite.validate_response import ValidateResponse
from compliance_suite.validate_drs_object_response import ValidateDRSObjectResponse
import json
import requests
from compliance_suite.helper import Parser
import os
from compliance_suite.constants import *
from compliance_suite.report_server import start_mock_server
from ga4gh.testbed.report.status import Status

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

drs_objects_access_id_map = {}

def report_runner(server_base_url, platform_name, platform_description, drs_version, config_file):
    """
    Returns a Report Object which is generated by running compliance tests on various endpoints of a DRS server.
    """
    # Read input DRS objects from config folder
    # TODO: Add lower and upper limits to input DRS objects
    config_service_info, config_drs_object_info, config_drs_object_access = get_config_json(config_file)

    # TODO: config json objects must contain auth_token and auth_type for service_info and for each of the drs_objects
    # get authentication information from respective config file based on type of authentication

    # Create a compliance report object
    report_object = Report()
    report_object.set_testbed_name(TESTBED_NAME)
    report_object.set_testbed_version(TESTBED_VERSION)
    report_object.set_testbed_description(TESTBED_DESCRIPTION)
    report_object.set_platform_name(platform_name)
    report_object.set_platform_description(platform_description)
    report_object.add_input_parameter("server_base_url",server_base_url)

    ### PHASE: /service-info
    service_info_phase = report_object.add_phase()
    service_info_phase.set_phase_name("service info")
    service_info_phase.set_phase_description("run all the tests for service_info endpoint")

    ### TEST: GET service-info
    test_service_info(
        service_info_phase,
        server_base_url,
        auth_type = config_service_info["auth_type"],
        auth_token = config_service_info["auth_token"],
        schema_dir = "",
        schema_file = SERVICE_INFO_SCHEMA,
        expected_status_code = "200",
        expected_content_type = "application/json")

    service_info_phase.set_end_time_now()

    # TODO : Add a test case to check that drs version from service-info == drs_version provided.
    schema_dir = "v" + drs_version

    # TODO: extend support to DRS v1.3.0 -
    #  1. make a json map of endpoints per each DRS version
    #  using which phases are created and added to the report object
    #  2. schema_dir should take care of pulling the right schema for validation
    #  3. Add the version to supported_drs_versions
    #  4. add any version specific test cases


    ### PHASE: /objects/{object_id}
    drs_object_phase = report_object.add_phase()
    drs_object_phase.set_phase_name("drs object info")
    drs_object_phase.set_phase_description("run all the tests for drs object info endpoint")

    for this_drs_object in config_drs_object_info:

        test_drs_object_info(
            drs_object_phase,
            server_base_url,
            this_drs_object,
            schema_dir = schema_dir
            )

    # TODO: add extra tests to check the case where auth is required but not provided,
    #  it should return an error response object with appropriate status code

    drs_object_phase.set_end_time_now()

    # PHASE: /objects/{object_id}/access/{access_id}
    drs_access_phase = report_object.add_phase()
    drs_access_phase.set_phase_name("drs object access")
    drs_access_phase.set_phase_description("run all the tests for drs access endpoint")

    for this_drs_object in config_drs_object_access:
        for this_access_id in drs_objects_access_id_map[this_drs_object["drs_id"]]:          
            test_drs_object_access(
                drs_access_phase,
                server_base_url,
                this_drs_object,
                drs_access_id = this_access_id,
                schema_dir = schema_dir)

    drs_access_phase.set_end_time_now()
    report_object.set_end_time_now()
    report_object.finalize()
    return report_object

def get_config_json(config_file):
    """
    Returns the auth details for service-info endpoint and input DRS objects from the config file.
    """
    try:
        with open(os.path.join(config_file), "r") as f:
            config = json.load(f)
            config_service_info = config["service_info"]
            config_drs_object_info = config["drs_object_info"]
            config_drs_object_access = config["drs_object_access"]
            return config_service_info, config_drs_object_info, config_drs_object_access
    except Exception as e:
        raise Exception(f"Failed loading JSON config file: {config_file}",e)

def test_service_info(
        service_info_phase,
        server_base_url,
        auth_type,
        auth_token,
        schema_dir,
        schema_file,
        expected_status_code,
        expected_content_type):

    service_info_test = service_info_phase.add_test()
    service_info_test.set_test_name(f"Run test cases on the service-info endpoint; auth_type = {auth_type}")
    service_info_test.set_test_description("validate service-info status code, content-type "
                                       "and response schemas")

    response = send_request(
        server_base_url,
        SERVICE_INFO_URL,
        auth_type,
        auth_token)

    add_common_test_cases(
        test_object = service_info_test,
        endpoint_name = "Service Info",
        response = response,
        expected_status_code = expected_status_code,
        expected_content_type = expected_content_type,
        schema_dir = schema_dir,
        schema_file = schema_file)

    service_info_test.set_end_time_now()

def test_drs_object_info(
        drs_object_phase,
        server_base_url,
        drs_object,
        schema_dir
        ):

    expected_content_type = "application/json"
    auth_type = drs_object["auth_type"]
    auth_token = drs_object["auth_token"]
    drs_object_id = drs_object["drs_id"]
    is_bundle = drs_object["is_bundle"]

    global drs_objects_access_id_map
    
    if "test_name" in drs_object:
        test_name_prefix = drs_object["test_name"] + " "
    else:
        test_name_prefix = ""

    drs_object_test = drs_object_phase.add_test()
    drs_object_test.set_test_name(f"{test_name_prefix}Run test cases on the drs object info endpoint for drs id = {drs_object_id}; auth_type = {auth_type}")
    drs_object_test.set_test_description("validate drs object status code, content-type and response schemas")
    endpoint_name = "DRS Object Info"

    response = send_request(
        server_base_url,
        DRS_OBJECT_INFO_URL + drs_object_id,
        auth_type,
        auth_token)

    if "is_fake" in drs_object and drs_object["is_fake"]:
        expected_status_code = "404"
        schema_file = ERROR_SCHEMA
        skip_access_methods_test_cases = True
        endpoint_name = "Invalid DRS ID test"
        skip_message = f"skipping access methods for {endpoint_name}"
    else:
        expected_status_code = "200"
        schema_file = DRS_OBJECT_SCHEMA		
        skip_access_methods_test_cases = False
        skip_message = ""

    status_code_pass = add_common_test_cases(
        test_object = drs_object_test,
        endpoint_name = endpoint_name,
        response = response,
        expected_status_code = expected_status_code,
        expected_content_type = expected_content_type,
        schema_dir = schema_dir,
        schema_file = schema_file)

    if is_bundle:

        # Response with expand parameter set to true
        response = send_request(
            server_base_url,
            DRS_OBJECT_INFO_URL + drs_object_id,
            auth_type,
            auth_token,
            expand = True)

        ### CASE: response expand bundle
        add_test_case_common(
            test_object = drs_object_test,
            case_type = "response_schema",
            case_name = "DRS Access expand bundle validation",
            case_description = f"Validate DRS bundle when expand = True",
            response = response,
            schema_name = os.path.join(schema_dir, DRS_BUNDLE_SCHEMA))

    add_access_methods_test_case(
        test_object = drs_object_test,
        case_type = "has_access_methods",
        case_description = f"Validate that {endpoint_name} response has "
                           f"access_methods field provided and that it is non-empty",
        endpoint_name = endpoint_name,
        response = response,
        skip_access_methods_test_cases = skip_access_methods_test_cases,
        skip_message = skip_message,
        is_bundle=is_bundle)

    drs_objects_access_id_map[drs_object_id] = add_access_methods_test_case(
        test_object = drs_object_test,
        case_type = "has_access_info",
        case_description =f"Validate that each access_method in the access_methods field "
                          f"of the {endpoint_name} response has at least one of 'access_url'"
                          f"or 'access_id' provided",
        endpoint_name = endpoint_name,
        response = response,
        skip_access_methods_test_cases = skip_access_methods_test_cases,
        skip_message = skip_message,
        is_bundle=is_bundle)

    drs_object_test.set_end_time_now()

def test_drs_object_access(
        drs_access_phase,
        server_base_url,
		drs_object,
		drs_access_id,
        schema_dir):

    expected_content_type = "application/json"
    auth_type = drs_object["auth_type"]
    drs_object_id = drs_object["drs_id"]
    
    if "test_name" in drs_object:
    	test_name_prefix = drs_object["test_name"] + " "
    else:
    	test_name_prefix = ""
    drs_access_test = drs_access_phase.add_test()
    drs_access_test.set_test_name(f"{test_name_prefix}Run test cases on the drs access endpoint for drs id = {drs_object_id} "
                                  f"and access id = {drs_access_id}; auth_type = {auth_type}")
    drs_access_test.set_test_description("validate drs access status code, content-type and response schemas")

    response = send_request(
        server_base_url,
        DRS_OBJECT_INFO_URL + drs_object_id + DRS_ACCESS_URL + drs_access_id,
        auth_type,
        drs_object["auth_token"])

    if "invalid_token" in drs_object and drs_object["invalid_token"]:
        expected_status_code = "403"
        schema_file = ERROR_SCHEMA
        endpoint_name = "DRS Access with invalid token"
    else:
        expected_status_code = "200"
        endpoint_name = "DRS Access"
        schema_file = DRS_ACCESS_SCHEMA

    add_common_test_cases(
        test_object = drs_access_test,
        endpoint_name = endpoint_name,
        response = response,
        expected_status_code = expected_status_code,
        expected_content_type = expected_content_type,
        schema_dir = schema_dir,
        schema_file = schema_file)

    drs_access_test.set_end_time_now()

def send_request(
        server_base_url,
        endpoint_url,
        auth_type,
        auth_token,
        **kwargs):

    request_body = {}
    headers = {}
    http_method = "GET"

    if auth_type == "passport":
        if endpoint_url != SERVICE_INFO_URL:
            # endpoints that allow auth_type: "passport"
            # 1. DRS Objects: /objects/{object_id}
            # 2. DRS Object Access: /objects/{object_id}/access/{access_id}
            request_body["passports"] = auth_token
            if ("expand" in kwargs) and (kwargs["expand"]):
                request_body["expand"] = True
            http_method = "POST"
        else:
            # Service Info endpoint allows "basic", "bearer", or "none" auth
            pass
    elif auth_type == "basic":
        headers = {"Authorization": "Basic {}".format(auth_token)}
    elif auth_type == "bearer":
        headers = {"Authorization": "Bearer {}".format(auth_token)}
    elif auth_type == "none":
        pass
    else:
        raise ValueError("Invalid auth_type")

    if 'expand' in kwargs.keys() and auth_type != "passport":
        params = {'expand': True}
    else:
        params = {}

    response = requests.request(
        method = http_method,
        url = server_base_url + endpoint_url,
        params = params,
        json = request_body,
        headers = headers)

    return response

def add_common_test_cases(
        test_object,
        endpoint_name,
        response,
        expected_status_code,
        expected_content_type,
        schema_dir,
        schema_file):
    """
    Adds common test cases to a Test object
    Common test cases:
        1. validate response status_code
        2. validate response content_type
        3. validate response json schema
    """

    ### CASE: response status_code
    status_code_pass = add_test_case_common(
        test_object = test_object,
        case_type = "status_code",
        case_name = f"{endpoint_name} response status code validation",
        case_description = f"Check if the response status code is {expected_status_code}",
        response = response,
        expected_status_code = expected_status_code)

    ### CASE: response content_type
    add_test_case_common(
        test_object = test_object,
        case_type = "content_type",
        case_name = f"{endpoint_name} response content-type validation",
        case_description = f"Check if the content-type is {expected_content_type}",
        response = response,
        expected_content_type = expected_content_type)

    ### CASE: response schema
    add_test_case_common(
        test_object = test_object,
        case_type = "response_schema",
        case_name = f"{endpoint_name} response schema validation",
        case_description = f"Validate {endpoint_name} response schema when status = {expected_status_code}",
        response = response,
        schema_name = os.path.join(schema_dir, schema_file))

    return status_code_pass

def add_test_case_common(test_object, case_type, **kwargs):
    """
    Adds a common test case to a Test object based on type of the case - status_code/ content_type/ response_schema.
    """
    test_case = test_object.add_case()
    test_case.set_case_name(kwargs['case_name'])
    test_case.set_case_description(kwargs['case_description'])

    validate_response = ValidateResponse()
    validate_response.set_case(test_case)
    validate_response.set_actual_response(kwargs['response'])

    if case_type == 'status_code':
        validate_response.validate_status_code(kwargs['expected_status_code'])
    elif case_type == 'content_type':
        validate_response.validate_content_type(kwargs['expected_content_type'])
    elif case_type == 'response_schema':
        validate_response.set_response_schema_file(kwargs['schema_name'])
        validate_response.validate_response_schema()
    test_case.set_end_time_now()
    if case_type == 'status_code':
        return test_case.get_status()

def add_access_methods_test_case(
        test_object,
        case_type,
        case_description,
        endpoint_name,
        response,
        skip_access_methods_test_cases,
        skip_message,
        is_bundle):
    """
    Adds a test case to a Test object to check if access information is present in the drs_object response.
    DRS v1.2.0 Spec - `access_methods`:
     - Required for single blobs; optional for bundles.
     - At least one of `access_url` and `access_id` must be provided.
    """
    test_case = test_object.add_case()
    test_case.set_case_name(f"{endpoint_name} has access information")
    test_case.set_case_description(case_description)

    validate_drs_response = ValidateDRSObjectResponse()
    validate_drs_response.set_case(test_case)
    validate_drs_response.set_actual_response(response)

    if skip_access_methods_test_cases:
        test_case.set_status_skip()
        test_case.set_message(skip_message)

    access_id_list = None
    if case_type == "has_access_methods":
        if is_bundle:
            test_case.set_status_skip()
            test_case.set_message("Skip this test case as access_methods is optional for a DRS Bundle")
        validate_drs_response.validate_has_access_methods()
    elif case_type == "has_access_info":
        access_id_list = validate_drs_response.validate_has_access_info(is_bundle)
    test_case.set_end_time_now()
    return access_id_list

def main():
    args = Parser.parse_args()

    output_report = report_runner(server_base_url = args.server_base_url,
                                platform_name = args.platform_name,
                                platform_description = args.platform_description,
                                drs_version = args.drs_version,
                                config_file = args.config_file)

    output_report_json = json.loads(output_report.to_json(pretty=True))

    if not os.path.exists("./output"):
        os.makedirs("./output")

    # write output report to file
    with open(args.report_path, 'w', encoding='utf-8') as f:
        json.dump(output_report_json, f, ensure_ascii=False, indent=4)

    if (args.serve):
        web_dir_path = os.path.join(os.path.dirname(__file__), 'web')
        with open(os.path.join(web_dir_path,"temp_report.json"), 'w', encoding='utf-8') as f:
            json.dump(output_report_json, f, ensure_ascii=False, indent=4)
        start_mock_server(args.serve_port)

if __name__=="__main__":
    main()