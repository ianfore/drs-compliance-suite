def helper_check_no_extra_attributes(case, expected_attributes_list, actual_attributes_list):
    is_extra_attributes = not (set(actual_attributes_list).issubset(set(expected_attributes_list)))
    if (is_extra_attributes):
        extra_attributes = set(actual_attributes_list).difference(set(expected_attributes_list))
        case.status = "FAIL"
        case.message = "drs object response has extra attributes - {} " \
                       "that are not defined in the DRS specification".format(extra_attributes)
    else:
        case.status = "PASS"
        case.message = "No undefined attributes are present in drs object response"
    return

def check_all_drs_object_info_attr(case):
    """
    verify that there are no attributes in drs_object response that are not specificied in the drs standard
    All drs object response attributes: ["id", "name", "self_uri", "size", "created_time", "updated_time",
        "version", "mime_type", "checksums", "access_methods", "contents", "description", "aliases"]
    """
    case.status = "UNKNOWN"
    drs_object_info_all_attr = [
        "id",
        "name",
        "self_uri",
        "size",
        "created_time",
        "updated_time",
        "version",
        "mime_type",
        "checksums",
        "access_methods",
        "contents",
        "description",
        "aliases" ]
    response_json = case.actual_response.json()
    helper_check_no_extra_attributes(case, drs_object_info_all_attr, response_json.keys())
    return
    #
    # is_extra_attributes = not (set(response_json.keys()).issubset(set(drs_object_info_all_attr)))
    # if (is_extra_attributes):
    #     extra_attributes = set(response_json.keys()).difference(set(drs_object_info_all_attr))
    #     case.status = "FAIL"
    #     case.message = "drs object response has extra attributes - {} " \
    #                    "that are not defined in the DRS specification".format(extra_attributes)
    #     return
    # case.status = "PASS"
    # case.message = "No undefined attributes are present in drs object response"
    # return

def check_all_drs_object_info_attr_types(case):
    """
    verify that all the (required & optional) attributes in drs_object info response are of expected data types
    All Attributes & their data types:
    {
        "id": str,
        "name": str,
        "self_uri": str,
        "size": int,
        "created_time": str,
        "updated_time": str,
        "version": str,
        "mime_type": str,
        "checksums": list,
        "access_methods": list,
        "contents": list,
        "description": str,
        "aliases": list
    }
    """
    case.status = "UNKNOWN"
    drs_object_info_all_attr_types_map = {
        "id": str,
        "name": str,
        "self_uri": str,
        "size": int,
        "created_time": str,
        "updated_time": str,
        "version": str,
        "mime_type": str,
        "checksums": list,
        "access_methods": list,
        "contents": list,
        "description": str,
        "aliases": list
    }
    response_json = case.actual_response.json()
    for this_attr in response_json.keys():
        if (this_attr in drs_object_info_all_attr_types_map):
            if (type(response_json[this_attr]) is drs_object_info_all_attr_types_map[this_attr]):
                case.log_message.append("Actual & Expected data type of {}: {}".format(
                    this_attr,
                    drs_object_info_all_attr_types_map[this_attr].__name__))
            else:
                case.status = "FAIL"
                failure_message = "Actual data type of {}: {}. Expected data type: {}. ".format(
                    this_attr,
                    type(response_json[this_attr]).__name__,
                    drs_object_info_all_attr_types_map[this_attr].__name__)
                case.log_message.append(failure_message)
                case.message = case.message + failure_message
        else:
            case.log_message.append("Skip checking the data type of '{}' as this attribute is not defined in the spec"
                                    .format(this_attr))
    if case.status!="FAIL":
        case.status = "PASS"
        case.message = "The data types of all the attributes in the drs object info response are as expected"
    return

def check_required_drs_object_info_attr(case):
    """
    verify that all the required attributes in drs_object info response are present
    Required attributes: ["id","self_uri","size","created_time","checksums"]
    """
    case.status = "UNKNOWN"
    drs_object_info_req_attr = ["id","self_uri","size","created_time","checksums"]
    response_json = case.actual_response.json()

    absent_attributes = set(drs_object_info_req_attr).difference(set(response_json.keys()))
    if (len(absent_attributes)):
        case.status = "FAIL"
        case.message = "Required attributes - {} are absent in the drs object info response for object_id = {}"\
            .format(absent_attributes, response_json["id"])
        return
    case.status = "PASS"
    case.message = "All the required attributes in the drs object info response are present"
    return

def check_required_drs_object_info_checksums_attr(case):
    """
    verify that 'checksums' attribute is present in the response and it is a list of 'checksum' objects
    checksum object:
        {
            checksum (string, required),
            type (string, required)
        }
    """
    case.status = "UNKNOWN"
    # assert that the required attributes in drs_object info response are present
    drs_object_info_checksums_req_attr = ["checksum","type"]
    response_json = case.actual_response.json()
    if ("checksums" not in response_json or type(response_json["checksums"])!= list):
        case.status = "FAIL"
        case.message = "checksums attribute is not present in the drs_object response or it is not a list."
        return

    for this_checksum_object in response_json["checksums"]:
        absent_attributes = set(drs_object_info_checksums_req_attr).difference(set(this_checksum_object.keys()))
        if (len(absent_attributes)):
            case.status = "FAIL"
            case.message = "Required attributes - {} are absent in the drs object info response -> checksums for object_id = {}" \
                .format(absent_attributes, response_json["id"])
            return
    case.status = "PASS"
    case.message = "All the required attributes in the drs object info response -> checksums are present"
    return

def check_drs_object_info_access_methods_attr(case):
    """
    'access_methods' is an optional attribute in the drs_object response
    verify that if 'access_methods' attribute is present, then it is a list of 'access_method' objects
        'access_method' object:
            {
                type (string, required),
                access_url (ACCESS_URL, optional),
                access_id (string, optional),
                region (string, optional)
            }
        either 'access_url' or 'access_id' must be present in an 'access_method' object
        'type' is required attribute.


    """
    case.status = "UNKNOWN"
    response_json = case.actual_response.json()

    # "access_methods" is optional. If it is not present, SKIP this case
    if ("access_methods" not in response_json):
        case.status = "SKIP"
        case.message = "access_methods is not present in the drs_object response. Skip checking the structure of access_methods"
        return

    # if "access_methods" is not a list, FAIL
    elif type(response_json["access_methods"])!= list:
        case.status = "FAIL"
        case.message = "access_methods attribute is not a list in the drs_object response"
        return
    else:

        # all attributes in "access_method"
        drs_object_info_access_methods_all_attr_map = {
            "type": str,
            "access_url" : dict,
            "access_id" : str,
            "region" : str
        }

        # required attributes in "access_method"
        drs_object_info_access_methods_req_attr = ["type"]

        # For each access_method object
        for this_access_method_object in response_json["access_methods"]:

            # check if there are extra fields that are not specified in the DRS spec
            is_extra_attributes = not (set(this_access_method_object.keys()).issubset(set(drs_object_info_access_methods_all_attr_map.keys())))
            if (is_extra_attributes):
                extra_attributes = set(this_access_method_object.keys()).difference(set(drs_object_info_access_methods_all_attr_map.keys()))
                case.status = "FAIL"
                case.message = "drs object response -> access_methods  has extra attributes - {} " \
                               "that are not defined in the DRS specification".format(extra_attributes)
                return

            # check if all the required attributes are present
            absent_attributes = set(drs_object_info_access_methods_req_attr).difference(set(this_access_method_object.keys()))
            if (len(absent_attributes)):
                case.status = "FAIL"
                case.message = "Required attributes - {} are absent in the drs object info response -> access_methods for object_id = {}" \
                    .format(absent_attributes, response_json["id"])
                return

            # either "access_id" or "access_url" must be present
            if not ("access_id" in this_access_method_object.keys() or "access_url" in this_access_method_object.keys()):
                case.status = "FAIL"
                case.message = "Either 'access_id' or 'access_url' must be present in an access_method object. " \
                               "But, one or both of them is missing for object_id = {}".format(response_json["id"])
                return

            # # check the datatypes of the access_method object's attributes
            # for this_access_method_attr in this_access_method_object:
            #






    return