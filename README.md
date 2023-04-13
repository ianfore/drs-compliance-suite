# drs-compliance-suite
Tests to verify the compliance of a DRS implementation with GA4GH Data Repository Service (DRS) specification. 
This compliance suite currently supports the following DRS versions and will aim to support future versions of DRS as well.
* DRS 1.2.0

## Installations
Python 3.x is required to run DRS Compliance Suite. We recomment using a virtual environment to run the compliance suite.

Install Python virtualenv package and create a new Python virtual environment
```
pip3 install virtualenv
python3 -m virtualenv drs_venv
```
To activate the virtual environment
```
source <path_to_virtual_env>/bin/activate
```
To deactivate or exit the virtual environment
```
deactivate
```

Install the packages from requirements.txt
```
cd drs-compliance-suite
pip install -r requirements.txt
```

Add PYTHONPATH to env variables
```
export PYTHONPATH=<absolute path to drs-compliance-suite>
```

## Running natively in a developer environment

* First spin up a DRS starter kit on port 8085 or a port of your choice. Make sure to specify the port number correctly in the next step.
* The following command will run the DRS complaince suite against the specified DRS implementation.
``` 
python compliance_suite/report_runner.py --server_base_url "http://localhost:8085/ga4gh/drs/v1" --platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification" --auth_type "basic" --drs_version "1.2.0" --serve --serve_port 56565
```
### Command Line Arguments

#### Required:
* **--server_base_url** : base url of the DRS implementation that is being tested by the compliance suite
* **--platform_name** : name of the platform hosting the DRS server
* **--platform_description** : description of the platform hosting the DRS server
* **--auth_type** : type of authentication used in the DRS server implementation. It can be one of the following -
  * "none"
  * "basic"
  * "bearer"
  * "passport"
* **--drs_version** : version of DRS implemented by the DRS server. It can be one of the following -
  * "1.2.0"
* **--serve** : If this flag is set, the output report is served as an html webpage.
* **--serve_port** : The port where the output report html is deployed when serve option is used. Default value = 57568 

Depending on the auth type selected, the appropriate credentials must be provided by the end user
* Example credentials may be found for the associated auth type
  * "basic" : compliance_suite/config/config_basic.json
  * "bearer" : compliance_suite/config/config_bearer.json
  * "passport" : compliance_suite/config/config_passport.json

## Running the compliance suite via Docker

### Pull the docker image from dockerhub
```
docker pull ga4gh/DRS-compliance-suite:{version}
```
{version} specifies the version of the docker image being pulled

### Spinning up a docker container
```
docker run -d -p 15800:15800 --name DRS-compliance-suite ga4gh/DRS-compliance-suite --server https://www.ebi.ac.uk/ena/cram/ --port 15800 --serve
```
#### Arguments:
- `--server` or `-s` (required). It is the url of the refget server being tested. At least one `--server` argument is required. Multiple can be provided.
- `--serve` (optional) It's default value is False. If `--serve` flag is True then the compliance report will be served on the specified port.
- `--port` (optional) It's default value is 15800. If `--port` is specified then this port has to be mapped and published on the docker container by changing the -p option of the docker run command. For example, if `--port 8080` is specified, then docker run command will be
```bash
docker run -d -p 8080:8080 --name refget-compliance-suite ga4gh/refget-compliance-suite --server https://www.ebi.ac.uk/ena/cram/ --port 8080 --serve
```
- `--json` or `--json_path` (optional) If this argument is '-' then the output json is flushed to standard output. If a valid path is provided then the output is written as a json file at the specified location.
- `--file_path_name` or `-fpn` (optional) It's default value is "web". This argument is required to create a ".tar.gz" format of the output json with the specified name.
- `--no-web` (optional) If `--no-web` flag is True then the ".tar.gz" output file creation will be skipped.

## Running the good mock server that follows DRS v1.2.0 specification on port 8085
```
python unittests/good_mock_server_v1.2.0.py --auth_type "none" --app_host "0.0.0.0" --app_port "8085"
```
Make sure that the good mock server is running smoothly by making a GET request to 
```
http://localhost:8085/ga4gh/drs/v1/service-info
```
You should get a response status of 200

## Running the good mock server that follows DRS v1.3.0 specification on port 8086
```
python unittests/good_mock_server_v1.3.0.py --auth_type "none" --app_host "0.0.0.0" --app_port "8086"
```

Make sure that the good mock server is running smoothly by making a GET request to
```
http://localhost:8086/ga4gh/drs/v1/service-info
```
You should get a response status of 200

### Command Line Arguments
#### Required:
* **--app_port** : port where the mock server is running
#### Optional:
* **--auth_type** : type of authentication. It can be one of the following -
  * "none"
  * "basic"
  * "bearer"
  * "passport"
* **--app_host** : name of the host where the mock server is running

## Running unittests for testing
Note: Both bad and good mock servers should be running beforehand
#### Running the mock servers
```
python unittests/good_mock_server_v1.2.0.py --auth_type "none" --app_host "0.0.0.0" --app_port "8085"
python unittests/good_mock_server_v1.3.0.py --auth_type "none" --app_host "0.0.0.0" --app_port "8086"
python unittests/bad_mock_server.py --auth_type "none" --app_host "0.0.0.0" --app_port "8088"
```

###### Running the tests with code coverage
```
pytest --cov=compliance_suite unittests/ 
```

## Running workflows
#### CWL
###### `cwltool`
```
cwltool --outdir output tools/cwl/drs_compliance_suite.cwl tools/cwl/drs_compliance_suite.cwl.json
```
Note: `output` is the subdirectory where the report will be saved, can be customized.
###### `dockstore`
```
dockstore tool launch --local-entry tools/cwl/drs_compliance_suite.cwl --json tools/cwl/drs_compliance_suite.cwl.json --script
```
Notes:
* Saves the output file in the outermost directory (`/drs-compliance-suite/`).
* `--script` is used to override `dockstore`'s requirement that every python package must match versions.

#### WDL
```
dockstore workflow launch --local-entry tools/wdl/drs_compliance_suite.wdl --json tools/wdl/drs_compliance_suite.wdl.json
```
Notes:
* Saves the output file in the folder created to run the workflow. Can `cd` into the folder to retrieve the report.
* Find this printed line once the workflow is complete (`...` are randomly generated IDs):
```
[YYYY-MM-DD HH:MM:SS,MS] [info] SingleWorkflowRunnerActor workflow finished with status 'Succeeded'.
{
  "outputs": {
    "drsComplianceReportWorkflow.createDrsComplianceReport.drs_compliance_report": "/private/var/folders/.../cromwell-executions/drsComplianceReportWorkflow/.../call-createDrsComplianceReport/execution/wdl-test-drs-compliance-report.json"
  },
  "id": "..."
}
```