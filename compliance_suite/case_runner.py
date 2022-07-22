from cases import Case
from service_info_compliance import check_status_code, check_content_type, check_required_service_info_attr, check_required_service_type_attr, check_required_organization_attr
import json
import requests

if __name__=="__main__":
    interactions_file_path="./compliance_suite/interactions/service_info.json"
    with open(interactions_file_path) as f:
        service_info_interactions = json.load(f)

    # for each interaction, send the request and verify if the response is as expected
    for interaction in service_info_interactions["interactions"]:
        request_http_method = interaction["request"]["method"]
        request_uri = interaction["request"]["uri"]
        response = requests.request(request_http_method, request_uri)

        case_status_code = Case(
            case_name="status_code",
            case_description="check if the service-info response is as expected",
            algorithm=check_status_code,
            actual_response=response,
            expected_response= interaction["response"]
        )

        case_content_type = Case(
            case_name="content-type",
            case_description="check if the response Content-Type is as expected",
            algorithm=check_content_type,
            actual_response=response,
            expected_response= interaction["response"]
        )

        case_required_service_info_attr = Case(
            case_name="required response fields",
            case_description="check if the response contains all the required attributes",
            algorithm=check_required_service_info_attr,
            actual_response=response,
            expected_response= interaction["response"]
        )

        check_required_service_type_attr = Case(
            case_name="required response service type fields",
            case_description="check if the response 'type' field contains all the required attributes",
            algorithm=check_required_service_type_attr,
            actual_response=response,
            expected_response= interaction["response"]

        )

        # import pdb;pdb.set_trace()