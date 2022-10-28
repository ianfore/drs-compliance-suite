import argparse

def parse_args():
    """
    define shell arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth_type",
                        required=False,
                        help="supported types are \"none\", \"basic\", \"bearer\" ",
                        type=str,
                        choices=["none","basic","bearer","passport"],
                        default="none")
    parser.add_argument("--app_host",
                        required=False,
                        help="name of the host where the mock server is running",
                        type=str,
                        default="0.0.0.0")
    parser.add_argument("--app_port",
                        required=True,
                        help="port where the mock server is running",
                        type=str)
    args = parser.parse_args()
    return (args)