import json
import os
import pprint

def write_drs_object(drs_object):
    obj_id = drs_object["id"]
    data = {}

    # Get the existing data
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'mock_drs_objects.py')

    with open(path, 'r') as json_file:
        data = json.load(json_file)

    data[obj_id] = drs_object

    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return drs_object

def get_all_drs_objects():
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'mock_drs_objects.py')

    with open(path, 'r') as json_file:
        data = json.load(json_file)

    return data

def get_drs_object(drs_id):
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'mock_drs_objects.py')

    with open(path, 'r') as json_file:
        data = json.load(json_file)
        
        # Check if object exists
        if drs_id in data:
            return data[drs_id]

def get_drs_access_url(drs_id, access_id, app_host, app_port):
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'mock_drs_object_bytes.py')

    with open(path, 'r') as json_file:
        data = json.load(json_file)
        
        # Check if object exists AND access ID is correct
        if drs_id in data and access_id in data[drs_id]:
            return_obj = {
                "url": "http://" + app_host + ":" + app_port + "/ga4gh/drs/v1/stream/" + drs_id + "/" + access_id
            }

            return return_obj

def get_drs_object_bytes(drs_id, access_id):
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'mock_drs_object_bytes.py')

    with open(path, 'r') as json_file:
        data = json.load(json_file)

        # Check if object exists AND access ID is correct
        if drs_id in data and access_id in data[drs_id]:
            return data[drs_id][access_id]