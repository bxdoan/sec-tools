import hashlib
import os
import bcrypt

HERE = os.path.dirname(os.path.abspath(__file__))
PW_LIST = f'{HERE}/../wordlists/ignis-10M.txt'

def md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def sha1_hash(password):
    return hashlib.sha1(password.encode()).hexdigest()

def sha256_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sha512_hash(password):
    return hashlib.sha512(password.encode()).hexdigest()

def bcrypt_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def save_password_and_all_hash(from_idx=0):
    # load password list from file
    with open(PW_LIST, 'r', encoding="utf8") as f:
        all_passwords = f.readlines()
        all_passwords = [password.strip() for password in all_passwords]

    passwords = all_passwords[from_idx:] if from_idx > 0 else all_passwords
    for idx, password in enumerate(passwords):
        line_text = f'{password},{md5_hash(password)},{sha1_hash(password)},{sha256_hash(password)},{sha512_hash(password)},{bcrypt_hash(password)}'
        print(f"{from_idx+idx+1}/{all_passwords} : {line_text}")
        with open(f'{HERE}/../data/pass_hashes.txt', 'a') as f:
            f.write(line_text + '\n')

if __name__ == '__main__':
    # save password and all hash
    save_password_and_all_hash(from_idx=354)
