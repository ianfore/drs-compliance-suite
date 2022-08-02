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
        # pprint.pprint(data)

    return data

def get_drs_object(drs_id):
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'mock_drs_objects.py')

    with open(path, 'r') as json_file:
        data = json.load(json_file)
        
        # Check if object exists
        if drs_id in data:
            # pprint.pprint(data[drs_id])
            return data[drs_id]
        # else:
        #     return False

def get_drs_access_url(drs_id, access_id):
    curr_dir = os.path.dirname(__file__) # returns drs-compliance-suite/unittests
    path = os.path.join(curr_dir, 'data', 'mock_access_methods.py')

    with open(path, 'r') as json_file:
        data = json.load(json_file)
        
        # Check if object exists AND access ID is correct
        if drs_id in data and data[drs_id]["accessId"] == access_id:
            return data[drs_id]["url"]