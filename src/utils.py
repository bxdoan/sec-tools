import copy
import subprocess
import time
from pywifi import ControlConnection
from dongle_lte_api import Dongle
import requests
from src.config import get_logger, NETWORK_PASSWORD, LIST_NETWORK, PATH_OF_AIRPORT

logger = get_logger(__name__)


def ip():
    try:
        ip = requests.get('https://checkip.amazonaws.com').text.strip()
    except Exception as _e:
        ip = ""
    return ip


def reboot():
    """ Reboot dongle """
    Dongle().reboot()


def change_network():
    """ Change network """
    try:
        logger.info(f"IP Address:     {ip()}")
        change_to_network = None
        while not change_to_network:
            try:
                change_to_network = get_network()
            except Exception as _e:
                logger.error(f"Error get network: {_e}, retry after 3s")
            time.sleep(3)
        logger.info(f"Change from {get_ssid()} to {change_to_network}")

        reboot()

        res = None
        while not res:
            try:
                res = ControlConnection(wifi_ssid=change_to_network, wifi_password=NETWORK_PASSWORD).wifi_connector()
            except Exception as _e:
                logger.error(f"Error connect {change_to_network}: {_e} retry after 10s")
            time.sleep(10)

        logger.info(f"New IP Address: {ip()}")
    except Exception as e:
        logger.error(f"Error change network: {e}")


def get_ssid():
    """Get the SSID of the connected WiFi."""
    process = subprocess.Popen([PATH_OF_AIRPORT, "-I"], stdout=subprocess.PIPE)
    out, err = process.communicate()
    process.wait()
    output = {}
    for line in out.decode("utf-8").split("\n"):
        if ": " in line:
            key, value = line.split(": ")
            key = key.strip()
            value = value.strip()
            output[key] = value

    return output["SSID"]


def get_network(exclude_network: str = None) -> str:
    """ Get network """
    if exclude_network is None:
        exclude_network = get_ssid()

    list_network = copy.deepcopy(LIST_NETWORK)
    if exclude_network in list_network:
        list_network.remove(exclude_network)
    logger.info(f"List network: {list_network}")
    network = list_network[0]
    return network
