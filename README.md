# drs-compliance-suite
Tests to verify the compliance of a DRS implementation with GA4GH DRS specification 

## Installations
Python 3.x is required to run DRS Compliance Suite.

## Running natively in a developer environment

* First spin up a DRS starter kit on port 5000 or a port of your choice. Make sure to specify the port number correctly in the next step.
* The following command will run the DRS complaince suite against the specified DRS implementation.
``` 
python compliance_suite/report_runner.py --server_base_url "http://localhost:5000/ga4gh/drs/v1" --platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification"
```
### Command Line Arguments
#### Required:
* **--server_base_url** : base url of the DRS implementation that is being tested by the compliance suite
* **--platform_name** : name of the platform hosting the DRS server
* **--platform_description** : description of the platform hosting the DRS server