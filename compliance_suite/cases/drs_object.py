def check_required_drs_object_info_attr(case):
    case.status = "UNKNOWN"
    # assert that the required attributes in drs_object info response are present
    drs_object_info_req_attr = ["id","self_uri","size","created_time","checksums"]
    response_json = case.actual_response.json()

    if (set(drs_object_info_req_attr).issubset(set(response_json.keys()))):
        case.status = "PASS"
        case.message = "All the required attributes in the drs object info response are present"
    else:
        case.status = "FAIL"
        # TODO: print response_json.keys() - service_info_attr
        case.message = "Required attributes - {} are absent in the drs object info response for object_id = {}"

def check_required_drs_object_info_checksums_attr(case):
    case.status = "UNKNOWN"
    # assert that the required attributes in drs_object info response are present
    drs_object_info_checksums_req_attr = ["checksum","type"]
    response_json = case.actual_response.json()
    # import pdb; pdb.set_trace()
    if ("checksums" not in response_json or type(response_json["checksums"])!= list):
        case.status = "FAIL"
        case.message = "checksums attribute is not present in the drs_object response or it is not a list."
        return

    for this_checksum in response_json["checksums"]:
        if (not set(drs_object_info_checksums_req_attr).issubset(set(this_checksum.keys()))):
            case.status = "FAIL"
            case.message = "Required attributes - {} are absent in the drs object info - checksums response for object_id = {}"
            return

    case.status = "PASS"
    case.message = "Required attributes - {} are present in the drs object info - checksums response for object_is = {}"