from cryptography.fernet import Fernet
import os

keyfile = 'key.key'

def get_key():
    file = open(keyfile, 'rb')
    key = file.read()
    file.close()
    return key


"""
 Creating Encryption key and store It
"""


def create_key():
    key = Fernet.generate_key()
    PATH = keyfile
    if not os.path.isfile(PATH) and not os.access(PATH, os.R_OK):
        file = open(keyfile, 'wb')
        file.write(key)
        file.close()
