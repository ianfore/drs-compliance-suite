def check_required_service_info_attr(case):
    case.status = "UNKNOWN"
    # assert that the required attributes in service-info are present
    service_info_req_attr = ["id","name","type","organization","version"]
    response_json = case.actual_response.json()

    # TODO: check if this logic is correct
    if (set(service_info_req_attr).issubset(set(response_json.keys()))):
        case.status = "PASS"
        case.message = "Required attributes - {} are present in the service info response"
    else:
        case.status = "FAIL"
        # TODO: print response_json.keys() - service_info_req_attr
        case.message = "Required attributes - {} are absent in the service info response"

def check_required_service_info_type_attr(case):
    case.status = "UNKNOWN"
    service_info_type_req_attr = ["group","artifact","version"]
    response_json = case.actual_response.json()
    
    # TODO: check - when type does not have keys, make sure it doesn't break the code

    # If "type" key doesn't exist, fail the case
    if "type" not in set(response_json):
        case.status = "FAIL"
        # TODO: print response_json.keys() - service_info_type_req_attr
        case.message = "Service info has no attribute 'type'"
    elif set(service_info_type_req_attr).issubset(set(response_json["type"].keys())):
        case.status = "PASS"
        case.message = "Required attributes - {} are present in the service info - type response"
    else:
        case.status = "FAIL"
        # TODO: print response_json.keys() - service_info_type_req_attr
        case.message = "Required attributes - {} are absent in the service info.type response"

def check_required_service_info_org_attr(case):
    case.status = "UNKNOWN"
    service_info_org_req_attr = ["name","url"]
    response_json = case.actual_response.json()

    if set(service_info_org_req_attr).issubset(set(response_json["organization"].keys())):
        case.status = "PASS"
        case.message = "Required attributes - {} are present in the service info - organization response"
    else:
        case.status = "FAIL"
        # TODO: print response_json.keys() - service_type_attr
        case.message.append = "Required attributes - {} are absent in the service info - organization response"