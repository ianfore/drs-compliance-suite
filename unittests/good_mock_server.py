from flask import Flask, request, Response
import json
import os
import re
import datetime
from constants import GOOD_SERVER_URL
from edit_data import *
from collections.abc import Mapping

good_server_host = GOOD_SERVER_URL.split("://")[1].split(":")[0]
good_server_port = GOOD_SERVER_URL.split("://")[1].split(":")[1].replace("/","")

app = Flask(__name__)

'''
HTTP codes
200:"Success"
206:"Success. Filtered Subsequence"
303:"Redirect to a url where sequence can be retrieved"
400:"Bad Request",
401:"Unauthorized",
404:"Not Found",
406:"Not Acceptable",
416:"Range Not Satisfiable",
501:"Not Implemented"
'''

# Get service info
@app.route('/ga4gh/drs/v1/service-info', methods=['GET'])
def get_service_info():
    header_content = request.headers
    accept_type = "application/json"

    # validate the accept header
    if "accept" in header_content and header_content["accept"] not in [accept_type, "*/*"]:
        return Response(status=406)

    service_info_resp = {
        "id": "org.ga4gh.starterkit.drs",
        "name": "GA4GH Starter Kit DRS Service",
        "description": "An open source, community-driven implementation of the GA4GH Data Repository Service (DRS) API specification.",
        "contactUrl": "mailto:info@ga4gh.org",
        "documentationUrl": "https://github.com/ga4gh/ga4gh-starter-kit-drs",
        "environment": "test",
        "version": "0.3.1",
        "type": {
            "group": "org.ga4gh",
            "artifact": "drs",
            "version": "1.1.0"
        },
        "organization": {
            "name": "Global Alliance for Genomics and Health",
            "url": "https://ga4gh.org"
        }
    }

    return Response(response=json.dumps(service_info_resp), status=200, mimetype=accept_type)

# GET Object or OPTS Endpoint
@app.route('/ga4gh/drs/v1/objects/<obj_id>', methods=['GET', 'OPTIONS'])
def get_object(obj_id):
    header_content = request.headers
    accept_type = "application/json"

    # validate the accept header
    if "accept" in header_content and header_content["accept"] not in [accept_type, "*/*"]:
        return Response(status=406)

    drs_obj = get_drs_object(obj_id)

    time_stamp = datetime.datetime.utcnow().isoformat()
    final_time_stamp = time_stamp[:time_stamp.find(".")] + "Z"

    if not drs_obj: # Object not found
        error_obj = {
            "timestamp": final_time_stamp,
            "status_code": 404,
            "error": "Not Found",
            "msg": "No DrsObject found by id: " + obj_id
        }

        return Response(response=json.dumps(error_obj), status=404, mimetype=accept_type)
    else:
        if request.method == 'GET':
            return Response(response=json.dumps(drs_obj), status=200, mimetype=accept_type)
        elif request.method == 'OPTIONS':
            opts_obj = {
                "supported_types": [
                    "None"
                ]
            }

            return Response(response=json.dumps(opts_obj), status=200, mimetype=accept_type)
        

# Get Access URL
@app.route('/ga4gh/drs/v1/objects/<obj_id>/access/<access_url>', methods=['GET'])
def get_access_url(obj_id, access_url):
    header_content = request.headers
    accept_type = "application/json"

    # validate the accept header
    if "accept" in header_content and header_content["accept"] not in [accept_type, "*/*"]:
        return Response(status=406)

    access_url = get_drs_access_url(obj_id, access_url)

    time_stamp = datetime.datetime.utcnow().isoformat()
    final_time_stamp = time_stamp[:time_stamp.find(".")] + "Z"

    if not access_url:
        # Object not found
        error_obj = {
            "timestamp": final_time_stamp,
            "status_code": 404,
            "error": "Not Found",
            "msg": "invalid access_id/object_id"
        }

        return Response(response=json.dumps(error_obj), status=404, mimetype=accept_type)
    else:
        # Object found
        return Response(response=json.dumps(access_url), status=200, mimetype=accept_type)

# Add new object
@app.route('/ga4gh/drs/v1/objects/', methods=['POST'])
def post_object():
    header_content = request.headers
    accept_type = "application/json"

    # validate the accept header
    if "accept" in header_content and header_content["accept"] not in [accept_type, "*/*"]:
        return Response(status=406)

    drs_obj = request.json

    time_stamp = datetime.datetime.utcnow().isoformat()
    final_time_stamp = time_stamp[:time_stamp.find(".")] + "Z"

    if not isinstance(drs_obj, Mapping): # Validate that it is a dictionary
        return Response(status=415)
    else:
        # Check if ID already exists
        data = get_all_drs_objects()
        if drs_obj["id"] in data:
            error_obj = {
                "timestamp": final_time_stamp,
                "status_code": 409,
                "error": "Conflict",
                "msg": "A(n) DrsObject already exists at id " + drs_obj["id"]
            }
            return Response(response=json.dumps(error_obj), status=409, mimetype=accept_type)

        # Add the drs object to the database
        write_drs_object(drs_obj)
        return Response(response=json.dumps(drs_obj), status=200, mimetype=accept_type) 

if __name__=="__main__":
    app.run(host="0.0.0.0",port=good_server_port)
