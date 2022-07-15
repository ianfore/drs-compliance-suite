from flask import Flask, request, Response
import json
import os
import re
from unittests.constants import GOOD_SERVER_URL

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

@app.route('/sequence/service-info', methods=['GET'])
def get_service_info():
    header_content = request.headers
    accept_type = "application/json"

    # validate the accept header
    if "accept" in header_content and header_content["accept"] not in [accept_type, "*/*"]:
        # bad mock server: status = 200 when headers are incorrect  
        return Response(status=200)

    # bad mock server: "type" key does not exist in the response
    service_info_resp = {
        "id": "org.ga4gh.starterkit.drs",
        "name": "GA4GH Starter Kit DRS Service",
        "description": "An open source, community-driven implementation of the GA4GH Data Repository Service (DRS) API specification.",
        "contactUrl": "mailto:info@ga4gh.org",
        "documentationUrl": "https://github.com/ga4gh/ga4gh-starter-kit-drs",
        "environment": "test",
        "version": "0.3.1",
        # "type": {
        #     "group": "org.ga4gh",
        #     "artifact": "drs",
        #     "version": "1.1.0"
        # },
        "organization": {
            "name": "Global Alliance for Genomics and Health",
            "url": "https://ga4gh.org"
        }
    }

    # bad mock server: status = 400 when success
    return Response(response=json.dumps(service_info_resp), status=400, mimetype=accept_type)