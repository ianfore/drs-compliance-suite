def check_status_code(case):
    case.status = "UNKNOWN"
    if (case.expected_response["status"]["code"] == case.actual_response.status_code):
        case.status = "PASS"
        case.message = "Response Status Code is as expected"
    else:
        case.status = "FAIL"
        case.message = "Response Status Code is not as expected"

def check_content_type(case):
    case.status = "UNKNOWN"

    if not case.actual_response.headers: # If there is no headers, fail
        case.status = "FAIL"
        case.message = "Headers is missing"
    elif "Content-Type" not in set(case.actual_response.headers): # If no Content-Type in headers, fail
        case.status = "FAIL"
        case.message = "Content-Type is missing in headers"
    elif (case.expected_response["headers"]["Content-Type"] == case.actual_response.headers["Content-Type"]):
        case.status = "PASS"
        case.message = "Response header 'Content-Type' is as expected"
    else:
        case.status = "FAIL"
        case.message = "Response header 'Content-Type' is not as expected"