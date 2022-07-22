def check_status_code(case):
    case.status = "UNKNOWN"
    if (case.expected_response["status"]["code"] == case.actual_response.status_code):
        case.status = "PASS"
    else:
        case.status = "FAIL"
    case.message = "Response Status Code is as expected"

def check_content_type(case):
    case.status = "UNKNOWN"
    if (case.expected_response["headers"]["Content-Type"] == case.actual_response.headers["Content-Type"]):
        case.status = "PASS"
    else:
        case.status = "FAIL"
    case.message = "Response header 'Content-Type' is as expected"

def check_required_service_info_attr(case):
    case.status = "UNKNOWN"
    # assert that the required attributes in service-info are present
    service_info_attr = case.expected_response["body"].keys()
    response_json = case.actual_response.json()

    if (set(service_info_attr).issubset(set(response_json.keys()))):
        case.status = "PASS"
        case.message = "All the required attributes in the service-info response are present"
    else:
        case.status = "FAIL"
        # TODO: print response_json.keys() - service_info_attr
        case.message = "Required attributes - {} are not present in the service-info response"

def check_required_service_type_attr(case):
    case.status = "UNKNOWN"
    service_type_attr = case.expected_response["body"]["type"].keys()
    response_json = case.actual_response.json()

    if set(service_type_attr).issubset(set(response_json["type"].keys())):
        case.status = "PASS"
        case.message = "All the required attributes in the service-info.type response are present"
    else:
        case.status = "FAIL"
        # TODO: print response_json.keys() - service_type_attr
        case.message = "Required attributes - {} are not present in the service-info.type response"

def check_required_organization_attr(case):
    case.status = "UNKNOWN"
    organization_attr = case.expected_response["body"]["organization"].keys()
    response_json = case.actual_response.json()

    if set(organization_attr).issubset(set(response_json["organization"].keys())):
        case.status = "PASS"
        case.message = "All the required attributes in the service-info.organization response are present"
    else:
        case.status = "FAIL"
        # TODO: print response_json.keys() - service_type_attr
        case.message.append = "Required attributes - {} are not present in the service-info.organization"