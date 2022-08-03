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