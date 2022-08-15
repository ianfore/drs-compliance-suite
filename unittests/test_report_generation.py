import os
import glob
import json
from resources.expected_reports import expected_good_mock_server_report
from resources.expected_reports import expected_bad_mock_server_report

def test_good_mock_server_report():
    # Generate a good mock report
    os.system('python3 compliance_suite/report_runner.py --server_base_url "http://0.0.0.0:8989/ga4gh/drs/v1" \
               --platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification"')

    # Find the last report
    curr_dir = os.path.dirname(os.path.dirname(__file__)) # returns drs-compliance-suite/
    output_path = os.path.join(curr_dir, 'output')

    reports_path = os.path.join(output_path, '*')
    list_of_reports = glob.glob(reports_path)
    latest_report = max(list_of_reports, key=os.path.getctime)
    
    # Load the latest report as a json
    good_mock_report = {}
    with open(os.path.join(output_path, latest_report)) as json_file:
        data = json.load(json_file)
        good_mock_report = data

    good_mock_reference = expected_good_mock_server_report
    assert validate_json(good_mock_report, good_mock_reference) is True

def test_bad_mock_server_report():
    # Generate a bad mock report
    os.system('python3 compliance_suite/report_runner.py --server_base_url "http://0.0.0.0:8988/ga4gh/drs/v1" \
               --platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification"')

    # Find the last report
    curr_dir = os.path.dirname(os.path.dirname(__file__)) # returns drs-compliance-suite/
    output_path = os.path.join(curr_dir, 'output')

    reports_path = os.path.join(output_path, '*')
    list_of_reports = glob.glob(reports_path)
    latest_report = max(list_of_reports, key=os.path.getctime)
    
    # Load the latest report as a json
    bad_mock_report = {}
    with open(os.path.join(output_path, latest_report)) as json_file:
        data = json.load(json_file)
        bad_mock_report = data

    bad_mock_reference = expected_bad_mock_server_report
    assert validate_json(bad_mock_report, bad_mock_reference) is True

def validate_json(actual_json, expected_json):
    '''
        Compares the actual_json to expected_json.
        actual_json should have all the keys and values in expected_json, actual_json can have extra keys/values.

        Example Cases:
        actual_json = {"a": 1}, expected_json = {"a": 1} --> PASS
        actual_json = {"a": 1, "b": 2}, expected_json = {"a": 1} --> PASS
        actual_json = {"a": 2}, expected_json = {"a": 1} --> FAIL
        actual_json = {"c": 1}, expected_json = {"a": 1} --> FAIL
    '''

    def validate_keys(actual_json, expected_json):
        for key in expected_json.keys():
            
            # actual_json needs to have the key
            if key not in actual_json.keys():
                # print("The key '" + key + "' doesn't exist in actual_json")
                return False

            if type(expected_json[key]) is dict:
                # recursively call the function again

                # if sub-section doesn't match, return False
                if not validate_keys(actual_json[key], expected_json[key]):
                    return False

            elif type(expected_json[key]) is list:

                # confirm same length list
                if len(expected_json[key]) != len(actual_json[key]):
                    return False

                # call recursively for each element in list
                for i in range(len(expected_json[key])):
                    if not validate_keys(actual_json[key][i], expected_json[key][i]):
                        return False

            elif not expected_json[key] == actual_json[key]:
                # print("The key " + key + " values aren't equal. In big: " + str(actual_json[key]) + ", in small: " + str(expected_json[key]))
                return False

        return True

    if type(actual_json) is not dict or type(expected_json) is not dict:
        # print("Please only enter JSON (dict) objects")
        return False

    return validate_keys(actual_json, expected_json)

# INTERNAL TESTS FOR THE validate_json METHOD

actual_json_0 = 5
expected_json_0 = 4
if not validate_json(actual_json_0, expected_json_0): # fail
    print('0')

actual_json_1 = {"a": 1}
expected_json_1 = {"a": 1}
if validate_json(actual_json_1, expected_json_1): # pass
    print('1')

actual_json_2 = {"a": 1, "b": 2}
if validate_json(actual_json_2, expected_json_1): # pass
    print('2')

actual_json_3 = {"a": 2}
if not validate_json(actual_json_3, expected_json_1): # fail
    print('3')

actual_json_4 = {"c": 1}
if not validate_json(actual_json_4, expected_json_1): # fail
    print('4')

actual_json_5 = {
    "first": {
        "a": 1,
        "b": 2
    }, 
    "second": 3
}
expected_json_2 = {
    "first": {
        "a": 1,
        "b": 2
    }, 
    "second": 3
}
if validate_json(actual_json_5, expected_json_2): # pass
    print('5')

actual_json_6 = {
    "first": {
        "a": 1,
        "b": 2
    }, 
    "second": {"a": 3}
}
if not validate_json(actual_json_6, expected_json_2): # fail
    print('6')

actual_json_7 = {
    "first": {
        "a": 1,
        "b": 2
    }, 
    "second": 3,
    "third": {"a": 4, "b": 5}
}
if validate_json(actual_json_7, expected_json_2): # pass
    print('7')