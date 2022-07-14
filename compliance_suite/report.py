# get the command line args -> drs server url
# run tests -> service_info.py
# get the output of service_info in the test phase format defined in testbed-lib
# return as json on std out
from helper import Parser, Logger

args = Parser.parse_args()
server_base_url = args.server_base_url
severity = args.log_level
print("server:" + server_base_url)
print("log level:" + severity)

logger = Logger.get_logger("WARN", "./logs/test.log", "dev")

logger.warning("WARN Testing!!!!!!",except_msg="test")
logger.info("INFO Testing!!!!!!",except_msg="test")
logger.debug("DEBUG Testing!!!!!!",except_msg="test")
logger.error("ERROR Testing!!!!!!",except_msg="test")



# TODO - plan
# for each endpoint, have a yml/json config kind of file that lists all the test cases -> endpoint name, inputs, headers,output
# json config use cases file structure
#   {
#   http_method: "",
#   endpoint:"",
#   url params:{"id":"","x":"","y":""},
#  headers:[],
# request_body:""
# }
# for each usecase - run requests.get(usecase) -> compare output is as expected