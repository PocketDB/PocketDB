import hashlib
from os import urandom
from hash_ops2 import get_sha1
from base64 import b64encode


def register_user(password, filename='encrypted', username='admin'):
    eusers = list_all_users()
    if username in eusers:
        return False
    fp = open(filename, 'a')
    fp.write(username)
    fp.write("\n")
    # fp.write(hashlib.sha224(password.encode('utf8')).hexdigest())
    fp.write(get_sha1(password))
    fp.write("\n")
    return True


def authenticate_user(password, filename='encrypted', username='admin'):
    fp = open(filename, 'r')
    lines = [i[:-1] for i in fp.readlines()]
    hashedPassword = ""
    for ii, i in enumerate(lines):
        if i == username:
            hashedPassword = lines[ii + 1]
            break
    return hashedPassword == get_sha1(password)


def list_all_users(filename='encrypted'):
    with open(filename, 'r') as f:
        c = 0
        allu = []
        for line in f.readlines():
            if c % 2 == 1:
                continue
            allu.append(line.strip())
            c += 1
    return allu


def authenticate(token):
    return authenticate_user(token)


def generate_new_token():
    with open('encrypted', 'w') as f:
        f.write('')
    rb = urandom(32)
    token = b64encode(rb).decode('utf-8')
    register_user(token)
    return token
