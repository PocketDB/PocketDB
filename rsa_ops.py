from Crypto.PublicKey import RSA
from Crypto import Random


def init_rsa():
    key = RSA.generate(4096, Random.new().read)
    pubkey = key.publickey()
    return pubkey.exportKey(), key.exportKey()
