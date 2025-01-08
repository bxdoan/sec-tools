import json, time
import os
from time import time_ns

import bcrypt

HERE = os.path.dirname(os.path.abspath(__file__))

def bcrypt_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def read_list_json(file_path):
    with open(file_path, 'r') as f:
        return json.loads(f.read())


if __name__ == '__main__':
    st = time.time()
    file_data = f'{HERE}/../data/gg/26.json'

    data = read_list_json(file_data)
    print(f"Data: {data}")
    time_in_h_m_s = time.strftime('%H:%M:%S', time.gmtime(time.time() - st))
    print(f"Time takes {time_in_h_m_s}")
