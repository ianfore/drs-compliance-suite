def check_required_drs_object_info_attr(case):
    case.status = "UNKNOWN"
    # assert that the required attributes in drs_object info response are present
    drs_object_info_req_attr = ["id","self_uri","size","created_time","checksums"]
    response_json = case.actual_response.json()

    # TODO: if expected response.status_code !=200 then skip


    if (set(drs_object_info_req_attr).issubset(set(response_json.keys()))):
        case.status = "PASS"
        case.message = "All the required attributes in the drs object info response are present"
    else:
        case.status = "FAIL"
        # TODO: print response_json.keys() - service_info_attr
        case.message = "Required attributes - {} are absent in the drs object info response for object_id = {}"

# for each item in checksums -> checksum, type are required