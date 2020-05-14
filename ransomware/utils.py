from random import randint
from os import urandom, remove
from .asymmetric_encryption import RSA
from .config import ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, MASTER_PUBLIC_KEY
from pickle import load, dump, HIGHEST_PROTOCOL


def write_data_to_file(file_path, data, serialized=True):
    file = open(file_path, "wb")
    if serialized:
        file.write(data)
    else:
        dump(data, file, HIGHEST_PROTOCOL)
    file.close()


def read_data_from_file(file_path, serialized=True):
    file = open(file_path, "rb")
    if serialized:
        file_data = file.read()
    else:
        file_data = load(file)
    file.close()
    return file_data


def shred_file(file_path):
    with open(file_path, "ab+") as file_to_be_deleted:
        length = file_to_be_deleted.tell()

    with open(file_path, "br+") as file_to_be_deleted:
        for _ in range(randint(3, 11)):
            file_to_be_deleted.seek(0)
            file_to_be_deleted.write(urandom(length))

    with open(file_path, "br+") as file_to_be_deleted:
        for x in range(length):
            file_to_be_deleted.write(b'\x00')

    remove(file_path)


def generate_rsa_key_pair():
    cipher = RSA()
    serialized_private_key = cipher.private_key
    serialized_public_key = cipher.public_key
    cipher = RSA(public_key=MASTER_PUBLIC_KEY)
    encrypted_private_key = cipher.encrypt_large_data(serialized_private_key)

    write_data_to_file(ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, encrypted_private_key, False)

    return serialized_public_key
