import logging
import os
from dotenv import load_dotenv

load_dotenv()

PATH_OF_AIRPORT = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"

NETWORK_PASSWORD = os.environ.get('NETWORK_PASSWORD')
NETWORK_NAME1    = os.environ.get('NETWORK_NAME1')
NETWORK_NAME2    = os.environ.get('NETWORK_NAME2')
LIST_NETWORK     = [NETWORK_NAME1, NETWORK_NAME2]


def get_logger(name):
    log = logging.getLogger(name)
    log.setLevel("DEBUG")

    # Create handlers
    c_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    # Configure the logger
    simple_format = logging.Formatter(
        "%(asctime)s [%(funcName)s() +%(lineno)d]: %(levelname)-8s %(message)s",
        datefmt="%b-%d %H:%M:%S%Z"
    )
    c_handler.setFormatter(simple_format)

    # Add handlers to the logger
    log.addHandler(c_handler)

    return log
