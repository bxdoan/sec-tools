import json, time
import os

import bcrypt

HERE = os.path.dirname(os.path.abspath(__file__))

def bcrypt_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def read_list_json(file_path):
    with open(file_path, 'r') as f:
        return json.loads(f.read())

def find_password_in_file(pw, lines):
    if not pw:
        return False
    for l in lines:
        l = l.strip()
        b_hash = bcrypt_hash(l)
        if pw == b_hash:
            return l
    return False

def process_account(i, file_hash_path, file_res_path):
    file_data = f'{HERE}/../data/gg/{i + 1}.txt'
    accounts = read_list_json(file_data)
    with open(file_hash_path, 'r', encoding='utf-8') as file, open(file_res_path, 'a') as out_file:
        lines = file.readlines()
        for idx, acc in enumerate(accounts):
            info = acc.get('email') or acc.get('nricfin') or acc.get('mobile')
            pw = acc.get('password')
            print (f"FILE {i+1} | Pools {len(lines)} | {idx+1}/{len(accounts)} | {acc['id']} : info={info} | PW {pw}")
            res = find_password_in_file(pw, lines)
            if res:
                print(f"Found password {info},{pw}")
                out_file.write(f"{info},{res}\n")


def process_account2(i, file_pass, file_res_path):
    file_data = f'{HERE}/../data/gg/{i + 1}.txt'
    accounts = read_list_json(file_data)
    with open(file_pass, 'r', encoding='utf-8') as file, open(file_res_path, 'a') as out_file:
        lines = file.readlines()
        for idx, acc in enumerate(accounts):
            info = acc.get('email') or acc.get('nricfin') or acc.get('mobile')
            pw = acc.get('password')
            print (f"FILE {i+1} | Pools {len(lines)} | {idx+1}/{len(accounts)} | {acc['id']} : info={info} | PW {pw}")
            res = find_password_in_file(pw, lines)
            if res:
                print(f"Found password {info},{pw}")
                out_file.write(f"{info},{res}\n")


if __name__ == '__main__':
    file_hash = f'{HERE}/../../../Documents/hashes.txt'
    file_pass = f'{HERE}/../wordlists/ignis-10M.txt'
    file_res = f'{HERE}/../data/res.txt'
    st = time.time()
    tasks = []
    for j in range(25):
        # process_account(j, file_hash, file_res)
        process_account2(j, file_pass, file_res)

    print(f"Processing {len(tasks)} files")
    time_in_h_m_s = time.strftime('%H:%M:%S', time.gmtime(time.time() - st))
    print(f"Time takes {time_in_h_m_s}")